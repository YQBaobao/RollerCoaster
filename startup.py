# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster
@ File        : startup.py
@ Author      : yqbao
@ version     : V1.0.0
@ Description :
"""
import asyncio
import sys

from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import QApplication
from asyncqt import QEventLoop

from lib.platform_version import get_windows_system_info
from core.rc import RollerCoasterApp
from core.rc_win11 import Win11FloatingRollerCoasterApp


class StartWindow(QObject):
    def __init__(self):
        super().__init__()
        # 启用 Qt 的高DPI支持
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 自动 DPI 缩放
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # 使用高分辨率图像资源

        self.app = QApplication(sys.argv)
        loop = QEventLoop(self.app)  # 创建 asyncio 事件循环
        asyncio.set_event_loop(loop)

        # 判断系统版本
        info = get_windows_system_info()
        if info.get('is_windows_11'):
            self.win11(loop)
        else:
            self.win10(loop)

    def win10(self, loop):
        rc = RollerCoasterApp()
        rc.show()
        self.app.aboutToQuit.connect(loop.stop)

        # 在 asyncio 事件循环中运行应用程序
        with loop:
            loop.run_forever()

    def win11(self, loop):
        rc = Win11FloatingRollerCoasterApp()
        rc.show()
        self.app.aboutToQuit.connect(loop.stop)

        # 在 asyncio 事件循环中运行应用程序
        with loop:
            loop.run_forever()
        # sys.exit(self.app.exec_())
