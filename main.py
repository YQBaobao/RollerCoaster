#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : main.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import sys

from PyQt5.QtCore import QObject, QFile
from PyQt5.QtWidgets import QApplication

from core.rc import RollerCoasterApp


class StartWindow(QObject):
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.rc = RollerCoasterApp()
        self.set_qss()
        self.rc.show()
        sys.exit(self.app.exec_())

    def set_qss(self):
        qss = QFile(':/qss/qss/rc.qss')
        if qss.open(QFile.ReadOnly | QFile.Text):
            style_bytearray = qss.readAll()  # 类型为 QByteArray
            style = str(style_bytearray, encoding='UTF-8')
            self.rc.setStyleSheet(style)
        qss.close()


if __name__ == '__main__':
    StartWindow()
