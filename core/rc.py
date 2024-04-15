#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster
@ File        : rc.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description :
"""
import time

import win32gui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QSystemTrayIcon, QMenu, QAction

from core.signals import BaseSignal
from core.snowball import Snowball
from uis.rc_ui import Ui_RollerCoaster
from static.rc_rc import qInitResources

qInitResources()


# noinspection PyUnresolvedReferences
class RollerCoasterApp(QWidget, Ui_RollerCoaster):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 窗口无边框

        self.base_signal = BaseSignal()
        self.snowball = Snowball()

        self.timer()
        self.tray_icon()
        self.init_ui()

    def init_ui(self):
        m_h_taskbar = win32gui.FindWindow("Shell_TrayWnd", None)  # 任务栏“Shell_TaryWnd”的窗口句柄
        m_h_bar = win32gui.FindWindowEx(m_h_taskbar, 0, "ReBarWindow32", None)  # 子窗口“ReBarWindow32”的窗口句柄
        m_h_min = win32gui.FindWindowEx(m_h_bar, 0, "MSTaskSwWClass", None)  # 子窗口“MSTaskSwWClass”的窗口句柄
        b = win32gui.GetWindowRect(m_h_bar)  # 获取m_hBar窗口尺寸b为[左，上，右，下]的数组
        win32gui.MoveWindow(m_h_min, 0, 0, b[2] - b[0] - 80, b[3] - b[1], True)  # 调整m_hMin的窗口大小，为我们的程序预留出位置

        self.setGeometry(b[2] - b[0] - 80, 0, 80, b[3] - b[1])  # 调整我们自己的窗口到预留位置的大小
        win32gui.SetParent(int(self.winId()), m_h_bar)  # 将我们自己的窗口设置为m_hBar的子窗口

        self.show()  # 显示窗口

    def timer(self, interval: int = 5000):
        self.time = QTimer(self)
        self.time.setInterval(interval)
        self.time.timeout.connect(self.show_value)

    def show_value(self):
        timestamp = int(time.time() * 1000)
        try:
            quote = self.snowball.quote(self.symbol, timestamp)
            current = quote['data'][0]['current']  # 当前价格
            percent = quote['data'][0]['percent']  # 跌涨幅度 %
            if percent > 0:
                self.setStyleSheet(
                    'QLabel#label_value,#label_rate{color: rgb(170, 0, 0);}font: 75 10pt "Adobe Arabic";')
            elif percent < 0:
                self.setStyleSheet(
                    'QLabel#label_value,#label_rate{color: rgb(0, 170, 0);}font: 75 10pt "Adobe Arabic";')
            else:
                self.setStyleSheet('QLabel#label_value,#label_rate{color: rgb(0, 0, 0);}font: 75 10pt "Adobe Arabic";')

            self.label_value.setText(str(current))
            self.label_rate.setText(str(percent) + '%')
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
        from core.setting import UiSettingQWidget

        self.base_signal.signal_symbol.connect(self.get_setting)
        self.setting = UiSettingQWidget(self.base_signal)
        self.setting.setWindowFlag(Qt.WindowContextHelpButtonHint, on=False)  # 取消帮助按钮
        self.setting.exec()

    def get_setting(self, data):
        self.setting.close()
        self.time.stop()  # 停止

        self.symbol = data['symbol']
        self.timer(data['interval'])
        self.time.start()  # 启动

    def tray_menu_quit(self):
        self.tray.hide()
        self.tray = None  # 清空托盘对象内存
        self.close()

    def closeEvent(self, event) -> None:
        try:
            self.time.stop()
            self.tray.hide()
            self.tray = None  # 清空托盘对象内存
        except Exception:
            pass
        super(RollerCoasterApp, self).closeEvent(event)
