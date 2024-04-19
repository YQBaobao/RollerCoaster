#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : base.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import os

from PyQt5.QtWidgets import QWidget, QListView, QMessageBox
from configobj import ConfigObj

from temp import TEMP
from uis.rc_setting.base.base import Ui_Base


class UiBaseQWidget(QWidget, Ui_Base):
    interval_time = [2000, 3000, 5000, 10000]  # 延迟

    def __init__(self, base_signal, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.base_signal = base_signal

        self.comboBox.setView(QListView())
        self.init_ui()

    def init_ui(self):
        file_path = os.path.join(TEMP, "user_data.ini")
        self.config = ConfigObj(file_path, encoding='UTF8')
        self.lineEdit.setText(self.config['base']['symbol'])
        self.comboBox.setCurrentText(self.config['base']['interval'])

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
        self.user_data_save()
        self.base_signal.signal_symbol.emit(data)

    def user_data_save(self):
        """保存在用户数据"""
        symbol = self.lineEdit.text()
        interval = self.comboBox.currentText()

        self.config['base']['symbol'] = symbol
        self.config['base']['interval'] = interval
        self.config.write()
