#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster
@ File        : rc.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 主类 rc
"""
import asyncio
import datetime
import os
import time

import psutil
import win32gui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor, QFont
from PyQt5.QtWidgets import QWidget, QSystemTrayIcon, QMenu, QAction
from configobj import ConfigObj
from system_hotkey import SystemHotkey

from core.message_box import MessageBox
from core.signals import BaseSignal
from core.snowball import Snowball, GuShiTong
from temp import TEMP
from uis.rc_ui import Ui_RollerCoaster
from static.rc_rc import qInitResources

qInitResources()


class RollerCoasterApp(QWidget, Ui_RollerCoaster):
    symbol = ['SZ002594']  # 默认
    current = [0]
    percent = [0]
    up = 'color: rgb(170, 0, 0);'
    down = 'color: rgb(0, 170, 0);'
    light = 'color: rgb(255, 255, 255);'
    dark = 'color: rgb(0, 0, 0);'
    open_setting = ('control', 'up')  # 默认快捷键
    show_data = ('control', 'down')
    red_green_switch = ('control', 'left')
    boss_key = ('control', 'right')
    shortcut_key_label = ['打开/关闭设置', '显示/隐藏任务栏数据', '绿变红（滑稽）', '老板键']

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 窗口无边框
        self.init_attribute()

        self.start_run()  # 重复启动检查
        self.timer()  # 请求定时
        self.timer_start(interval=1 * 60 * 1000)  # 收盘后定时,1分钟
        self.timer_polling()  # 交替
        self.timer_set_taskbar()  # 定时设置任务栏
        self.tray_icon()  # 托盘
        self.init_ui()  # 初始化UI
        self.init_action()  # 动作
        self.init_shortcut_key()  # 快捷键

    def init_attribute(self):
        self.setting_is_active_window = False
        self.start_status = True
        self.default_style = self.light  # 默认白
        self.down_style = self.down  # 默认绿
        self.polling_status = 1
        self.background_button = True  # 背景色按钮状态
        self.msg_status = True  # 消息提醒状态
        self.check_update_status = False  # 未检查更新的标志

        self.base_signal = BaseSignal()
        self.snowball = Snowball()
        self.gu_shi_tong = GuShiTong()
        self.message_box = MessageBox()

        self.user_data_path = os.path.join(TEMP, "user_data.ini")
        # 不存在用户数据，则新建
        if not os.path.exists(self.user_data_path):
            try:
                os.mkdir(os.path.dirname(self.user_data_path))
            except Exception:
                pass
            with open(self.user_data_path, "w") as f:
                user_data = (
                    '[base]\nsymbol = SZ002594\nsymbol_2=\nsymbol_3=\nsymbol_4=\nmode = 1\ninterval = 2000\n\n'
                    '[background_color]\ncolor = "#101010"\n\n'
                    '[shortcut_key]\nopen_setting = control+up\nshow_data = control+down\n'
                    'red_green_switch = control+left\nboss_key = control+right\n\n'
                    '[config]\nbackground_button = false\n\n'
                    '[update]\ncheck = gitee')
                f.write(user_data)

    def init_ui(self):
        font = QFont()
        font.setPointSize(10)
        self.label_value.setFont(font)
        self.label_rate.setFont(font)
        self.set_taskbar()  # 初始化

        self.config = ConfigObj(self.user_data_path, encoding='UTF8')
        color = QColor(self.config['background_color']['color'])
        palette = self.palette()
        palette.setColor(QPalette.Background, color)
        self.setPalette(palette)
        self.label_value.setStyleSheet(self.light)
        self.label_rate.setStyleSheet(self.light)

    def set_taskbar(self):
        """设置任务栏"""
        self.m_h_taskbar = win32gui.FindWindow("Shell_TrayWnd", None)  # 任务栏“Shell_TaryWnd”的窗口句柄
        self.m_h_bar = win32gui.FindWindowEx(self.m_h_taskbar, 0, "ReBarWindow32",
                                             None)  # 子窗口“ReBarWindow32”的窗口句柄
        self.m_h_min = win32gui.FindWindowEx(self.m_h_bar, 0, "MSTaskSwWClass", None)  # 子窗口“MSTaskSwWClass”的窗口句柄
        self.b = win32gui.GetWindowRect(self.m_h_bar)  # 获取m_hBar窗口尺寸b为[左，上，右，下]的数组

        self.move_window()

    def move_window(self):
        # 调整m_hMin的窗口大小，为我们的程序预留出位置
        win32gui.MoveWindow(self.m_h_min, 0, 0, self.b[2] - self.b[0] - 55, self.b[3] - self.b[1], True)

        self.setGeometry(self.b[2] - self.b[0] - 55, -6, 55, self.b[3] - self.b[1])  # 调整我们自己的窗口到预留位置的大小
        win32gui.SetParent(int(self.winId()), self.m_h_bar)  # 将我们自己的窗口设置为m_hBar的子窗口

    def timer_set_taskbar(self, interval: int = 200):  # 500ms
        """定时设置任务栏"""
        self.time_set_taskbar = QTimer(self)
        self.time_set_taskbar.setInterval(interval)
        self.time_set_taskbar.timeout.connect(self.get_taskbar_size)
        self.time_set_taskbar.start()  # 启动

    def get_taskbar_size(self):
        """获取任务栏尺寸"""
        self.b_new = win32gui.GetWindowRect(self.m_h_bar)
        if self.b_new == self.b:  # 尺寸没变化，则直接返回
            return
        self.b = self.b_new
        self.move_window()

    def init_action(self):
        """信号"""
        self.base_signal.signal_symbol.connect(self.set_base)
        self.base_signal.signal_background_color.connect(self.set_background_color)
        self.base_signal.signal_setting_close.connect(self.close_setting)
        self.base_signal.signal_shortcut_key.connect(self.set_shortcut_key)
        self.base_signal.signal_shortcut_key_update.connect(self.init_shortcut_key)  # 更新快捷键

        self.base_signal.signal_msg_status.connect(self.msg_status_f)

        self.base_signal.signal_check_tags.connect(self.check_update_tags)  # 更新标签

    def msg_status_f(self):
        self.msg_status = False

    def init_shortcut_key(self):
        # 获取用户数据
        config = ConfigObj(self.user_data_path, encoding='UTF8')
        self.open_setting = self.shortcut_key_format(config['shortcut_key']['open_setting'])
        self.show_data = self.shortcut_key_format(config['shortcut_key']['show_data'])
        self.red_green_switch = self.shortcut_key_format(config['shortcut_key']['red_green_switch'])
        self.boss_key = self.shortcut_key_format(config['shortcut_key']['boss_key'])

        # 初始化快捷键
        self._init_shortcut_key(SystemHotkey(), self.open_setting, 1)
        self._init_shortcut_key(SystemHotkey(), self.show_data, 2)
        self._init_shortcut_key(SystemHotkey(), self.red_green_switch, 3)
        self._init_shortcut_key(SystemHotkey(), self.boss_key, 4)

    def _init_shortcut_key(self, key: SystemHotkey, button, v):
        try:
            key.register(button, callback=lambda x: self.keypress_callback(v))
        except Exception:
            pass

    @staticmethod
    def shortcut_key_format(shortcut_key=''):
        key = shortcut_key.split('+')
        return key

    def timer(self, interval: int = 5000):
        self.time = QTimer(self)
        self.time.setInterval(interval)
        self.time.timeout.connect(lambda: self.get_value(self.symbol))

    def timer_start(self, interval: int = 3 * 60 * 1000):
        """启动定时器"""
        self.time_start = QTimer(self)
        self.time_start.setInterval(interval)
        self.time_start.timeout.connect(self.start)
        self.time_start.start()  # 启动

    def timer_polling(self, interval: int = 1000):
        """交替定时，默认1秒"""
        self.time_polling = QTimer(self)
        self.time_polling.setInterval(interval)
        self.time_polling.timeout.connect(
            lambda: self.show_value_polling(self.symbol, self.down_style, self.default_style))

    def get_value(self, symbols: list):
        try:
            self.current, self.percent = [], []
            timestamp = int(time.time() * 1000)
            symbol = ','.join(symbols)
            quotes = self.snowball.quote(symbol, timestamp)
            for quote in quotes['data']:
                current = quote['current']  # 当前价格
                percent = quote['percent']  # 跌涨幅度 %
                self.current.append(current)
                self.percent.append(percent)
            if self.get_trade_status == "已收盘":
                self.time.stop()
        except Exception:
            self.label_value.setText('错误')

    def show_value_polling(self, symbols, down_style, default_style):
        """交替显示"""
        try:
            if len(symbols) == 1:  # 仅一只，则不做任何处理
                self.set_color(self.current[-1], self.percent[-1], down_style, default_style)
                return
            if self.mode == 1:
                if len(symbols) == 2:
                    if self.polling_status == 1:
                        self.set_color(self.current[0], self.percent[0], down_style, default_style)
                        self.polling_status = 2
                    else:
                        self.set_color(self.current[-1], self.percent[-1], down_style, default_style)
                        self.polling_status = 1
                    return
                if len(symbols) == 3:
                    if self.polling_status == 1:
                        self.set_color(self.current[0], self.percent[0], down_style, default_style)
                        self.polling_status = 2
                    elif self.polling_status == 2:
                        self.set_color(self.current[1], self.percent[1], down_style, default_style)
                        self.polling_status = 3
                    else:
                        self.set_color(self.current[2], self.percent[2], down_style, default_style)
                        self.polling_status = 1
                    return
                if len(symbols) == 4:
                    if self.polling_status == 1:
                        self.set_color(self.current[0], self.percent[0], down_style, default_style)
                        self.polling_status = 2
                    elif self.polling_status == 2:
                        self.set_color(self.current[1], self.percent[1], down_style, default_style)
                        self.polling_status = 3
                    elif self.polling_status == 3:
                        self.set_color(self.current[2], self.percent[2], down_style, default_style)
                        self.polling_status = 4
                    else:
                        self.set_color(self.current[3], self.percent[3], down_style, default_style)
                        self.polling_status = 1
            elif self.mode == 2:
                if len(symbols) == 2:
                    self.set_color_mode_2(
                        self.current[0], self.current[1], self.percent[0], self.percent[1], down_style, default_style)
                    return
                if len(symbols) == 3:
                    if self.polling_status == 1:
                        self.set_color_mode_2(
                            self.current[0], self.current[1], self.percent[0], self.percent[1], down_style,
                            default_style)
                        self.polling_status = 2
                    else:
                        self.set_color_mode_2(self.current[2], '', self.percent[2], 0, down_style, default_style)
                        self.polling_status = 1
                if len(symbols) == 4:
                    if self.polling_status == 1:
                        self.set_color_mode_2(
                            self.current[0], self.current[1], self.percent[0], self.percent[1], down_style,
                            default_style)
                        self.polling_status = 2
                    else:
                        self.set_color_mode_2(
                            self.current[2], self.current[3], self.percent[2], self.percent[3], down_style,
                            default_style)
                        self.polling_status = 1
            else:
                if len(symbols) == 2:
                    self.set_color_mode_3(self.percent[0], self.percent[1], down_style, default_style)
                    return
                if len(symbols) == 3:
                    if self.polling_status == 1:
                        self.set_color_mode_3(self.percent[0], self.percent[1], down_style, default_style)
                        self.polling_status = 2
                    else:
                        self.set_color_mode_3(self.percent[2], 0, down_style, default_style)
                        self.polling_status = 1
                if len(symbols) == 4:
                    if self.polling_status == 1:
                        self.set_color_mode_3(self.percent[0], self.percent[1], down_style, default_style)
                        self.polling_status = 2
                    else:
                        self.set_color_mode_3(self.percent[2], self.percent[3], down_style, default_style)
                        self.polling_status = 1
        except Exception:
            pass

    def set_color(self, current, percent, down_style, default_style):
        if percent > 0:
            self.label_value.setStyleSheet(self.up)
            self.label_rate.setStyleSheet(self.up)
        elif percent < 0:
            self.label_value.setStyleSheet(down_style)
            self.label_rate.setStyleSheet(down_style)
        else:
            self.label_value.setStyleSheet(default_style)
            self.label_rate.setStyleSheet(default_style)
        self.label_value.setText(str(current))
        self.label_rate.setText(str(percent) + '%')

    def set_color_mode(self, percent_1, percent_2, down_style, default_style):
        if percent_1 > 0:
            self.label_value.setStyleSheet(self.up)
        elif percent_1 < 0:
            self.label_value.setStyleSheet(down_style)
        else:
            self.label_value.setStyleSheet(default_style)

        if percent_2 > 0:
            self.label_rate.setStyleSheet(self.up)
        elif percent_2 < 0:
            self.label_rate.setStyleSheet(down_style)
        else:
            self.label_rate.setStyleSheet(default_style)

    def set_color_mode_2(self, current_1, current_2, percent_1, percent_2, down_style, default_style):
        """显示模式2"""
        self.set_color_mode(percent_1, percent_2, down_style, default_style)
        self.label_value.setText(str(current_1))
        self.label_rate.setText(str(current_2))

    def set_color_mode_3(self, percent_1, percent_2, down_style, default_style):
        """显示模式3"""
        self.set_color_mode(percent_1, percent_2, down_style, default_style)
        self.label_value.setText(str(percent_1) + '%')
        self.label_rate.setText(str(percent_2) + '%')

    def tray_icon(self):
        """系统托盘"""
        self.tray = QSystemTrayIcon(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/rc/images/lined_up_32px.png"), QIcon.Normal, QIcon.Off)
        self.tray.setIcon(icon)
        self.tray.activated.connect(self.tray_icon_activated)

        tray_menu = QMenu()
        setting = QAction(QIcon('exit.png'), u'设置', self)  # 添加一级菜单动作选项
        open_license = QAction(QIcon('exit.png'), u'开源许可', self)
        quit_ = QAction(QIcon('exit.png'), u'退出', self)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/rc/images/setting.png"), QIcon.Normal, QIcon.Off)
        setting.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/rc/images/open_license.png"), QIcon.Normal, QIcon.Off)
        open_license.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/rc/images/quit.png"), QIcon.Normal, QIcon.Off)
        quit_.setIcon(icon)
        tray_menu.addAction(setting)
        tray_menu.addAction(open_license)
        tray_menu.addAction(quit_)
        setting.triggered.connect(self.tray_menu_setting)
        open_license.triggered.connect(self.tray_menu_license)
        quit_.triggered.connect(self.tray_menu_quit)
        self.tray.setContextMenu(tray_menu)  # 把tray_menu设定为托盘的右键菜单
        self.tray.show()

    def tray_icon_activated(self, reason):
        """托盘图标事件"""
        if reason == QSystemTrayIcon.DoubleClick:  # 双击
            # 若是最小化，则正常显示窗口,若不是最小化，则最小化
            self.showNormal() if self.isMinimized() or not self.isVisible() else self.showMinimized()

    def tray_menu_setting(self):
        if self.setting_is_active_window:  # 避免重复New
            self.setting.activateWindow()  # 激活
            return
        from core.rc_setting.setting import UiSettingQWidget

        self.setting = UiSettingQWidget(self.base_signal, background_button=self.background_button,
                                        msg_status=self.msg_status)
        self.setting.setWindowFlag(Qt.WindowContextHelpButtonHint, on=False)  # 取消帮助按钮
        if hasattr(self, 'tags'):
            self.setting.set_check_update(self.tags)
        if not self.check_update_status:  # 只用请求一次
            asyncio.create_task(self.setting.check_update())  # 检查新版本，在事件循环中运行异步函数
            self.check_update_status = True  # 已经检查更新的标志
        self.setting_is_active_window = True
        self.setting.exec()

    def tray_menu_license(self):
        """开源协议"""
        from core.openLicense.open_license import UiOpenLicenseQWidget

        open_license_dialog = UiOpenLicenseQWidget(self)
        open_license_dialog.setWindowFlag(Qt.WindowContextHelpButtonHint, on=False)  # 取消帮助按钮
        open_license_dialog.exec()

    def tray_menu_quit(self):
        self.tray.hide()
        self.tray = None  # 清空托盘对象内存
        self.close()

    def close_setting(self):
        self.setting_is_active_window = False

    def set_base(self, data):
        """基础"""
        self.time.stop()  # 停止

        self.symbol = data['symbol']
        self.timer(data['interval'])
        self.mode = data['mode']
        self.time.start()  # 启动
        self.start()  # 首次

        self.config = ConfigObj(self.user_data_path, encoding='UTF8')
        background_button = self.config['config']['background_button']
        if background_button.lower() != 'true':
            self.background_button = False  # 开启此行，则本次启动将再也不能修改背景色
        self.setting.pushButton_background_color.setEnabled(self.background_button)

        self.time_polling.stop()
        self.timer_polling(1200)  # 固定间隔
        self.time_polling.start()

    def set_background_color(self, data: QColor):
        """背景色"""
        palette = self.palette()
        palette.setColor(QPalette.Background, data)
        self.setPalette(palette)
        self.default_style = self.dark if '#eeeeee' == data.name() else self.light

    def set_shortcut_key(self, data):
        if data == 1:
            try:
                self.setting.close() if self.setting.isActiveWindow() else self.tray_menu_setting()
            except Exception:
                self.tray_menu_setting()  # 显示设置
            return
        if data == 2:
            # 若是最小化，则正常显示窗口,若不是最小化，则最小化
            self.showNormal() if self.isMinimized() or not self.isVisible() else self.showMinimized()
            return
        if data == 3:
            self.down_style = self.up if self.down_style == self.down else self.down
            return
        if data == 4:
            try:
                if self.setting.isActiveWindow():
                    self.setting.close()
            except Exception:
                pass
            if not self.isMinimized():
                self.showMinimized()
            return

    def keypress_callback(self, v):
        self.base_signal.signal_shortcut_key.emit(v)

    def start(self):
        self.get_trade_status = self.gu_shi_tong.get_trade_status(symbol=self.symbol[-1])
        hour = datetime.datetime.now().hour
        if self.get_trade_status == '已收盘':
            return
        if hour < 9 or 15 < hour:
            self.start_status = True  # 重置启动状态
            self.time.stop()  # 停止
            return
        if self.start_status:  # 修复定时器 time 的重复启动
            self.time.start()  # 启动
        self.start_status = False

    def check_update_tags(self, tags):
        self.tags = tags  # 保存下来

    @staticmethod
    def start_run(name='RoCoaster.exe'):
        """重复启动检查"""
        try:
            # 找到所有同名进程的PID
            pids = [pid.pid for pid in psutil.process_iter() if pid.name() == name]
            if len(pids) > 1:
                for pid in pids[:-1]:  # 结束除了最后一个之外的所有进程
                    psutil.Process(pid).terminate()  # 结束进程
        except (OSError, psutil.NoSuchProcess) as e:
            print("Error ending existing process:", e)

    def closeEvent(self, event) -> None:
        try:
            print('Close Event')
            if hasattr(self, "setting"):
                self.setting.close()
            if hasattr(self, "tray"):
                self.tray = None  # 清空托盘对象内存
            self.time_set_taskbar.stop()
            self.time_start.stop()
            self.time_polling.stop()
            self.time.stop()
        except Exception as e:
            print('Close Error: ', e)
        super(RollerCoasterApp, self).closeEvent(event)
