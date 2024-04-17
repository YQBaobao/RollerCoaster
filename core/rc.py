#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster
@ File        : rc.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description :
"""
import datetime
import os
import time

import win32gui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor, QKeySequence
from PyQt5.QtWidgets import QWidget, QSystemTrayIcon, QMenu, QAction, QShortcut

from core.signals import BaseSignal
from core.snowball import Snowball, GuShiTong
from uis.rc_ui import Ui_RollerCoaster
from static.rc_rc import qInitResources

qInitResources()


class RollerCoasterApp(QWidget, Ui_RollerCoaster):
    symbol = 'SZ002594'  # 默认
    up = 'color: rgb(170, 0, 0);'
    down = 'color: rgb(0, 170, 0);'
    light = 'color: rgb(255, 255, 255);'
    dark = 'color: rgb(0, 0, 0);'

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 窗口无边框
        self.setting_is_active_window = False
        self.start_status = True
        self.default_style = self.light  # 默认白

        self.base_signal = BaseSignal()
        self.snowball = Snowball()
        self.gu_shi_tong = GuShiTong()

        self.timer()  # 请求定时
        self.timer_start()  # 收盘后定时
        self.tray_icon()  # 托盘
        self.init_ui()  # 初始化UI
        self.init_action()  # 动作
        self.init_shortcut_key()  # 快捷键

    def init_ui(self):
        m_h_taskbar = win32gui.FindWindow("Shell_TrayWnd", None)  # 任务栏“Shell_TaryWnd”的窗口句柄
        m_h_bar = win32gui.FindWindowEx(m_h_taskbar, 0, "ReBarWindow32", None)  # 子窗口“ReBarWindow32”的窗口句柄
        m_h_min = win32gui.FindWindowEx(m_h_bar, 0, "MSTaskSwWClass", None)  # 子窗口“MSTaskSwWClass”的窗口句柄
        b = win32gui.GetWindowRect(m_h_bar)  # 获取m_hBar窗口尺寸b为[左，上，右，下]的数组
        win32gui.MoveWindow(m_h_min, 0, 0, b[2] - b[0] - 75, b[3] - b[1], True)  # 调整m_hMin的窗口大小，为我们的程序预留出位置

        self.setGeometry(b[2] - b[0] - 75, -5, 75, b[3] - b[1])  # 调整我们自己的窗口到预留位置的大小
        win32gui.SetParent(int(self.winId()), m_h_bar)  # 将我们自己的窗口设置为m_hBar的子窗口

        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(16, 16, 16))
        self.setPalette(palette)
        self.label_value.setStyleSheet(self.light)
        self.label_rate.setStyleSheet(self.light)

    def init_action(self):
        """信号"""
        self.base_signal.signal_symbol.connect(self.set_base)
        self.base_signal.signal_background_color.connect(self.set_background_color)
        self.base_signal.signal_setting_close.connect(self.close_setting)
        self.base_signal.signal_shortcut_key.connect(self.set_shortcut_key)

    def init_shortcut_key(self):
        from configobj import ConfigObj
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../temp/user_data.ini")
        config = ConfigObj(file_path, encoding='UTF8')
        open_setting = config['shortcut_key']['open_setting']
        show_data = config['shortcut_key']['show_data']
        red_green_switch = config['shortcut_key']['red_green_switch']
        boss_key = config['shortcut_key']['boss_key']

        QShortcut(QKeySequence(open_setting), self, lambda: self.base_signal.signal_shortcut_key.emit(1))
        QShortcut(QKeySequence(show_data), self, lambda: self.base_signal.signal_shortcut_key.emit(2))
        QShortcut(QKeySequence(red_green_switch), self, lambda: self.base_signal.signal_shortcut_key.emit(3))
        QShortcut(QKeySequence(boss_key), self, lambda: self.base_signal.signal_shortcut_key.emit(4))

    def timer(self, interval: int = 5000):
        self.time = QTimer(self)
        self.time.setInterval(interval)
        self.time.timeout.connect(lambda: self.show_value(self.default_style))

    def timer_start(self, interval: int = 3 * 60 * 1000):
        """启动定时器"""
        self.time_start = QTimer(self)
        self.time_start.setInterval(interval)
        self.time_start.timeout.connect(self.start)
        self.time_start.start()  # 启动

    def show_value(self, style):
        timestamp = int(time.time() * 1000)
        try:
            quote = self.snowball.quote(self.symbol, timestamp)
            current = quote['data'][0]['current']  # 当前价格
            percent = quote['data'][0]['percent']  # 跌涨幅度 %
            if percent > 0:
                self.label_value.setStyleSheet(self.up)
                self.label_rate.setStyleSheet(self.up)
            elif percent < 0:
                self.label_value.setStyleSheet(self.down)
                self.label_rate.setStyleSheet(self.down)
            else:
                self.label_value.setStyleSheet(style)
                self.label_rate.setStyleSheet(style)

            self.label_value.setText(str(current))
            self.label_rate.setText(str(percent) + '%')
            if self.get_trade_status == "已收盘":
                self.time.stop()
        except Exception:
            self.label_value.setText('错误')

    def tray_icon(self):
        """系统托盘"""
        self.tray = QSystemTrayIcon(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/rc/images/lined_up_32px.png"), QIcon.Normal, QIcon.Off)
        self.tray.setIcon(icon)
        self.tray.activated.connect(self.tray_icon_activated)

        tray_menu = QMenu()
        setting = QAction(QIcon('exit.png'), u'设置', self)  # 添加一级菜单动作选项
        quit_ = QAction(QIcon('exit.png'), u'退出', self)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/rc/images/setting.png"), QIcon.Normal, QIcon.Off)
        setting.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/rc/images/quit.png"), QIcon.Normal, QIcon.Off)
        quit_.setIcon(icon)
        tray_menu.addAction(setting)
        tray_menu.addAction(quit_)
        setting.triggered.connect(self.tray_menu_setting)
        quit_.triggered.connect(self.tray_menu_quit)
        self.tray.setContextMenu(tray_menu)  # 把tray_menu设定为托盘的右键菜单
        self.tray.show()

    def tray_icon_activated(self, reason):
        """托盘图标事件"""
        if reason == QSystemTrayIcon.DoubleClick:  # 双击
            if self.isMinimized() or not self.isVisible():
                self.showNormal()  # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
                self.activateWindow()
                return
            self.showMinimized()  # 若不是最小化，则最小化
            return

    def tray_menu_setting(self):
        if self.setting_is_active_window:  # 避免重复New
            self.setting.show()
            return
        from core.rc_setting.setting import UiSettingQWidget

        self.setting = UiSettingQWidget(self.base_signal)
        self.setting.setWindowFlag(Qt.WindowContextHelpButtonHint, on=False)  # 取消帮助按钮

        self.setting_is_active_window = True
        self.setting.exec()

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

    def set_background_color(self, data: QColor):
        """背景色"""
        palette = self.palette()
        palette.setColor(QPalette.Background, data)
        self.setPalette(palette)
        self.default_style = self.dark if '#eeeeee' == data.name() else self.light

    def set_shortcut_key(self, data):
        if data == 1:
            self.tray_menu_setting()
        print(data)
        return

    def start(self):
        self.get_trade_status = self.gu_shi_tong.get_trade_status(symbol=self.symbol)
        hour = datetime.datetime.now().hour
        if self.get_trade_status == '已收盘' and (hour < 9 or 15 <= hour):
            return
        if self.start_status:  # 修复定时器 time 的重复启动
            self.time.start()  # 启动
        self.start_status = False

    def tray_menu_quit(self):
        self.tray.hide()
        self.tray = None  # 清空托盘对象内存
        self.close()

    def closeEvent(self, event) -> None:
        try:
            self.setting.close()
            self.time.stop()
            self.tray.hide()
            self.tray = None  # 清空托盘对象内存
        except Exception:
            pass
        super(RollerCoasterApp, self).closeEvent(event)
