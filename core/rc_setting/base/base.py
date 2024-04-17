#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : base.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from PyQt5.QtWidgets import QWidget, QListView, QMessageBox

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
        msg = '请确认任务栏中，“数据”背景色是否与系统任务栏颜色一致？\n“确认”后将无法再修改背景色！'
        message = QMessageBox(QMessageBox.Information, '确认框', msg, QMessageBox.Yes | QMessageBox.No, parent=self)
        message.button(QMessageBox.Yes).setText("确认")
        message.button(QMessageBox.No).setText("取消")
        message.exec()
        if message.clickedButton() != message.button(QMessageBox.Yes):
            return
        symbol = self.lineEdit.text()
        interval = self.comboBox.currentIndex()
        data = {
            'symbol': symbol,
            'interval': self.interval_time[interval]
        }
        self.base_signal.signal_symbol.emit(data)
