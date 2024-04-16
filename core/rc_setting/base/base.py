#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : base.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from PyQt5.QtWidgets import QWidget, QListView

from uis.rc_setting.base.base import Ui_Base


class UiBaseQWidget(QWidget, Ui_Base):
    interval_time = [2000, 3000, 5000, 10000]  # 延迟

    def __init__(self, base_signal, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.base_signal = base_signal

        self.comboBox.setView(QListView())

    def setting_base(self):
        """基础设置"""
        symbol = self.lineEdit.text()
        interval = self.comboBox.currentIndex()
        data = {
            'symbol': symbol,
            'interval': self.interval_time[interval]
        }
        self.base_signal.signal_symbol.emit(data)
