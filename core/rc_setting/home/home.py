#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : home.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from PyQt5.QtWidgets import QWidget

from uis.rc_setting.home.home import Ui_Home


class UiHomeQWidget(QWidget, Ui_Home):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
