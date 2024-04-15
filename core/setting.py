#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : setting.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from PyQt5.QtWidgets import QDialog

from uis.setting_ui import Ui_Settiing


class UiSettingQWidget(QDialog, Ui_Settiing):
    interval_time = [2000, 3000, 5000, 10000]  # 延迟

    def __init__(self, base_signal, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.base_signal = base_signal

        self.pushButton.clicked.connect(self.setting)

    def setting(self):
        symbol = self.lineEdit.text()
        interval = self.comboBox.currentIndex()
        data = {
            'symbol': symbol,
            'interval': self.interval_time[interval]
        }
        self.base_signal.signal_symbol.emit(data)
