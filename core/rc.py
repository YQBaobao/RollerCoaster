#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster
@ File        : rc.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 主类 rc
"""
import datetime
import os
import time

import psutil
import win32gui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor
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
        self.timer_start()  # 收盘后定时
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
                    '[base]\nsymbol = SZ002594\nsymbol_2=\ninterval = 2000\n\n'
                    '[background_color]\ncolor = "#101010"\n\n'
                    '[shortcut_key]\nopen_setting = control+up\nshow_data = control+down\n'
                    'red_green_switch = control+left\nboss_key = control+right')
                f.write(user_data)

    def init_ui(self):
        self.set_taskbar()  # 初始化

        config = ConfigObj(self.user_data_path, encoding='UTF8')
        color = QColor(config['background_color']['color'])
        palette = self.palette()
        palette.setColor(QPalette.Background, color)
        self.setPalette(palette)
        self.label_value.setStyleSheet(self.light)
        self.label_rate.setStyleSheet(self.light)

    def timer_set_taskbar(self, interval: int = 5000):  # >3 秒。时间过短会导致推动图标异常
        """定时设置任务栏"""
        self.time_find_taskbar = QTimer(self)
        self.time_find_taskbar.setInterval(interval)
        self.time_find_taskbar.timeout.connect(self.set_taskbar)
        self.time_find_taskbar.start()  # 启动

    def set_taskbar(self):
        """设置任务栏"""
        m_h_taskbar = win32gui.FindWindow("Shell_TrayWnd", None)  # 任务栏“Shell_TaryWnd”的窗口句柄
        m_h_bar = win32gui.FindWindowEx(m_h_taskbar, 0, "ReBarWindow32", None)  # 子窗口“ReBarWindow32”的窗口句柄
        m_h_min = win32gui.FindWindowEx(m_h_bar, 0, "MSTaskSwWClass", None)  # 子窗口“MSTaskSwWClass”的窗口句柄
        b = win32gui.GetWindowRect(m_h_bar)  # 获取m_hBar窗口尺寸b为[左，上，右，下]的数组
        win32gui.MoveWindow(m_h_min, 0, 0, b[2] - b[0] - 75, b[3] - b[1], True)  # 调整m_hMin的窗口大小，为我们的程序预留出位置

        self.setGeometry(b[2] - b[0] - 75, -5, 75, b[3] - b[1])  # 调整我们自己的窗口到预留位置的大小
        win32gui.SetParent(int(self.winId()), m_h_bar)  # 将我们自己的窗口设置为m_hBar的子窗口

    def init_action(self):
        """信号"""
        self.base_signal.signal_symbol.connect(self.set_base)
        self.base_signal.signal_background_color.connect(self.set_background_color)
        self.base_signal.signal_setting_close.connect(self.close_setting)
        self.base_signal.signal_shortcut_key.connect(self.set_shortcut_key)
        self.base_signal.signal_shortcut_key_update.connect(self.init_shortcut_key)  # 更新快捷键

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
            for symbol in symbols:
                quote = self.snowball.quote(symbol, timestamp)
                current = quote['data'][0]['current']  # 当前价格
                percent = quote['data'][0]['percent']  # 跌涨幅度 %
                self.current.append(current)
                self.percent.append(percent)
            if self.get_trade_status == "已收盘":
                self.time.stop()
        except Exception:
            self.label_value.setText('错误')

    def show_value_polling(self, symbols, down_style, default_style):
        """交替显示"""
        try:
            if len(symbols) == 1:  # 不交替
                current, percent = self.current[-1], self.percent[-1]
                self.set_color(current, percent, down_style, default_style)
                return
            if len(symbols) == 2 and self.polling_status % 2 != 0:
                current, percent = self.current[0], self.percent[0]
                self.set_color(current, percent, down_style, default_style)
                self.polling_status = 2
            else:
                current, percent = self.current[-1], self.percent[-1]
                self.set_color(current, percent, down_style, default_style)
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

        self.setting = UiSettingQWidget(self.base_signal)
        self.setting.setWindowFlag(Qt.WindowContextHelpButtonHint, on=False)  # 取消帮助按钮

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
        self.time.start()  # 启动
        self.start()  # 首次
        self.setting.pushButton_background_color.setEnabled(False)

        self.time_polling.stop()
        self.timer_polling(data['interval'] / 2)
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
        if self.get_trade_status == '已收盘' and (hour < 9 or 15 <= hour):
            return
        if self.start_status:  # 修复定时器 time 的重复启动
            self.time.start()  # 启动
        self.start_status = False

    @staticmethod
    def start_run(name='RoCoaster.exe'):
        """重复启动检查"""
        try:
            pids = psutil.process_iter()
            pids_ = []
            for pid in pids:
                if pid.name() == name:
                    pids_.append(pid.pid)
            if len(pids_) > 1:
                for i in range(0, len(pids_) - 1):
                    os.system('taskkill /f /PID {}'.format(pids_[i]))  # 结束进程
        except OSError as e:
            print("Error ending existing process:", e)

    def closeEvent(self, event) -> None:
        try:
            self.setting.close()
            self.time_start.stop()
            self.time_polling.stop()
            self.time.stop()
            self.tray.hide()
            self.tray = None  # 清空托盘对象内存
        except Exception:
            pass
        super(RollerCoasterApp, self).closeEvent(event)
