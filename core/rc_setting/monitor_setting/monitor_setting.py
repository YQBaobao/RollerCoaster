#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster 
@ File        : monitor_setting.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from PyQt5.QtWidgets import QWidget

from uis.rc_setting.monitor_setting.monitor_setting import Ui_Monitor


class UiMonitorQWidget(QWidget, Ui_Monitor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
