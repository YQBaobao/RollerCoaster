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

from core.message_box import MessageBox
from temp import TEMP
from uis.rc_setting.base.base import Ui_Base


class UiBaseQWidget(QWidget, Ui_Base):
    interval_time = [2000, 3000, 5000, 10000]  # 延迟

    def __init__(self, base_signal, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.base_signal = base_signal
        self.msg_status = True  # 是否提示消息

        self.comboBox.setView(QListView())
        self.message_box = MessageBox()
        self.init_ui()

    def init_ui(self):
        file_path = os.path.join(TEMP, "user_data.ini")
        self.config = ConfigObj(file_path, encoding='UTF8')
        self.lineEdit.setText(self.config['base']['symbol'])
        self.lineEdit_2.setText(self.config['base']['symbol_2'])
        self.comboBox.setCurrentText(self.config['base']['interval'])

    def setting_base(self):
        """基础设置"""
        symbol = self.lineEdit.text()
        symbol_2 = self.lineEdit_2.text()
        if symbol == symbol_2:
            self.message_box.info_message('“代码(1)”与“代码(2)”不能相同。', self)
            return
        if not symbol:
            self.message_box.info_message('“代码(1)”必须有值。', self)
            return
        if self.msg_status:
            background_button = self.config['config']['background_button']
            if background_button.lower() != 'true':
                msg = '请确认任务栏中，“数据”背景色是否与系统任务栏颜色一致？\n“确认”后将无法再修改背景色！'
            else:
                msg = '请确认代码是否填写正确？'
            message = QMessageBox(QMessageBox.Information, '确认框', msg,
                                  QMessageBox.Yes | QMessageBox.No | QMessageBox.Close,
                                  parent=self)
            message.button(QMessageBox.Yes).setText("确认")
            message.button(QMessageBox.No).setText("取消")
            message.button(QMessageBox.Close).setText("不在提示")
            message.exec()
            if message.clickedButton() == message.button(QMessageBox.No):
                return
            if message.clickedButton() == message.button(QMessageBox.Close):
                self.msg_status = False
        interval = self.comboBox.currentIndex()
        data = {'interval': self.interval_time[interval]}
        if not symbol_2:
            data['symbol'] = [symbol]
        else:
            data['symbol'] = [symbol, symbol_2]
        self.user_data_save()
        self.base_signal.signal_symbol.emit(data)

    def user_data_save(self):
        """保存在用户数据"""
        symbol = self.lineEdit.text()
        interval = self.comboBox.currentText()
        symbol_2 = self.lineEdit_2.text()

        self.config['base']['symbol'] = symbol
        self.config['base']['symbol_2'] = symbol_2
        self.config['base']['interval'] = interval
        self.config.write()
