#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : main.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import asyncio
import sys

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication
from asyncqt import QEventLoop

from core.rc import RollerCoasterApp


class StartWindow(QObject):
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        loop = QEventLoop(self.app)  # 创建 asyncio 事件循环
        asyncio.set_event_loop(loop)

        self.rc = RollerCoasterApp()
        self.rc.show()
        self.app.aboutToQuit.connect(loop.stop)

        with loop:
            loop.run_forever()  # 在 asyncio 事件循环中运行应用程序
        # sys.exit(self.app.exec_())


if __name__ == '__main__':
    StartWindow()
