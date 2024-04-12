#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster
@ File        : rc.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description :
"""

import win32gui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QSystemTrayIcon, QMenu, QAction

from core.rc_ui import UiRollerCoaster
from static.rc_rc import qInitResources

qInitResources()


class RollerCoasterApp(QWidget, UiRollerCoaster):
    def __init__(self):
        super().__init__()
        self.setup_ui(self)
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
        self.setWindowFlags(Qt.FramelessWindowHint)  # 窗口无边框
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)  # 窗口置顶，无边框
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)  # 窗口置顶，无边框，在任务栏不显示图标
        # self.setStyleSheet("QLabel{color: white;}")

        self.tray_icon()
        self.init_ui()

    def init_ui(self):
        m_h_taskbar = win32gui.FindWindow("Shell_TrayWnd", None)  # 任务栏“Shell_TaryWnd”的窗口句柄
        m_h_bar = win32gui.FindWindowEx(m_h_taskbar, 0, "ReBarWindow32", None)  # 子窗口“ReBarWindow32”的窗口句柄
        m_h_min = win32gui.FindWindowEx(m_h_bar, 0, "MSTaskSwWClass", None)  # 子窗口“MSTaskSwWClass”的窗口句柄
        b = win32gui.GetWindowRect(m_h_bar)  # 获取m_hBar窗口尺寸b为[左，上，右，下]的数组
        win32gui.MoveWindow(m_h_min, 0, 0, b[2] - b[0] - 160, b[3] - b[1], True)  # 调整m_hMin的窗口大小，为我们的程序预留出位置

        self.setGeometry(b[2] - b[0] - 160, 0, 160, b[3] - b[1])  # 调整我们自己的窗口到预留位置的大小
        win32gui.SetParent(int(self.winId()), m_h_bar)  # 将我们自己的窗口设置为m_hBar的子窗口

        self.show()  # 显示窗口

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
        if reason == QSystemTrayIcon.Trigger:  # 单击
            if self.isMinimized() or not self.isVisible():
                self.showNormal()  # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
                self.activateWindow()
                return
            self.showMinimized()  # 若不是最小化，则最小化
            return

    def tray_menu_setting(self):
        pass

    def tray_menu_quit(self):
        self.tray.hide()
        self.tray = None  # 清空托盘对象内存
        self.close()

    def closeEvent(self, event) -> None:
        try:
            self.tray.hide()
            self.tray = None  # 清空托盘对象内存
        except Exception:
            pass
        super(RollerCoasterApp, self).closeEvent(event)
