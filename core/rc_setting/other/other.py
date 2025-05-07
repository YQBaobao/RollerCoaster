# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster
@ File        : other.py
@ Author      : yqbao
@ version     : V1.0.0
@ Description :
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from uis.rc_setting.other.other import Ui_Other


class UiOtherQWidget(QWidget, Ui_Other):
    def __init__(self, base_signal, parent=None, ):
        super().__init__(parent)
        self.setupUi(self)
        self.base_signal = base_signal
