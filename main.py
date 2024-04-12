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

from PyQt5.QtWidgets import QApplication

from core.rc import RollerCoasterApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RollerCoasterApp()
    sys.exit(app.exec_())
