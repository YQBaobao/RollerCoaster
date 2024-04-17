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

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication

from core.rc import RollerCoasterApp


class StartWindow(QObject):
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.rc = RollerCoasterApp()
        self.rc.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    StartWindow()
