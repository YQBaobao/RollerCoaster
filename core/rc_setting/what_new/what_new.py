#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : what_new.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from PyQt5.QtWidgets import QWidget

from uis.rc_setting.what_new.what_new import Ui_WhatNew


class UiWhatNewQWidget(QWidget, Ui_WhatNew):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
