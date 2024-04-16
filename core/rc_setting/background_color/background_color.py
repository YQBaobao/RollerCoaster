#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : background_color.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from PyQt5.QtWidgets import QWidget

from uis.rc_setting.background_color.backgroud_color import Ui_BackgroundColor


class UiBackgroundColorQWidget(QWidget, Ui_BackgroundColor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
