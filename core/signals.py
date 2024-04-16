#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : signals.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from PyQt5.QtCore import QObject, pyqtSignal


class BaseSignal(QObject):
    signal_symbol = pyqtSignal(dict)
    signal_background_color = pyqtSignal(str)
