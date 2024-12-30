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
import typing

from PyQt5.QtWidgets import QWidget, QListView, QMessageBox
from configobj import ConfigObj

from core.message_box import MessageBox
from temp import TEMP
from uis.rc_setting.base.base import Ui_Base


class UiBaseQWidget(QWidget, Ui_Base):
    interval_time = [2000, 3000, 4000, 6000, 8000, 10000]  # 延迟

    def __init__(self, base_signal, parent=None, msg_status=True):
        super().__init__(parent)
        self.setupUi(self)
        self.base_signal = base_signal
        self.msg_status = msg_status  # 是否提示消息

        self.mode = 1  # 显示模式
        self.buttonGroup.buttonClicked.connect(self.on_button_clicked)
        self.comboBox.setView(QListView())
        self.message_box = MessageBox()
        self.init_ui()

    def on_button_clicked(self, button):
        """显示模式"""
        if button.objectName() == self.radioButton.objectName():
            self.mode = 1
        elif button.objectName() == self.radioButton_2.objectName():
            self.mode = 2
        else:
            self.mode = 3

    def init_ui(self):
        self.user_data_path = os.path.join(TEMP, "user_data.ini")
        self.config = ConfigObj(self.user_data_path, encoding='UTF8')
        self.lineEdit.setText(self.config['base']['symbol'])
        self.lineEdit_2.setText(self.config['base']['symbol_2'])
        try:
            self.lineEdit_3.setText(self.config['base']['symbol_3'])
            self.lineEdit_4.setText(self.config['base']['symbol_4'])
            mode = int(self.config['base']['mode'])
            if mode == 1:
                self.radioButton.setChecked(True)
            elif mode == 2:
                self.radioButton_2.setChecked(True)
            else:
                self.radioButton_3.setChecked(True)
        except KeyError:
            pass
        self.comboBox.setCurrentText(self.config['base']['interval'])

    def setting_base(self):
        """基础设置"""
        symbol_1 = self.lineEdit.text().strip()
        symbol_2 = self.lineEdit_2.text().strip()
        symbol_3 = self.lineEdit_3.text().strip()
        symbol_4 = self.lineEdit_4.text().strip()
        symbol_list = self.data_verification(symbol_1, symbol_2, symbol_3, symbol_4)
        if not symbol_list:
            return
        if self.msg_status:
            if not self.msg():
                return
        interval = self.comboBox.currentIndex()
        data = {'interval': self.interval_time[interval], 'symbol': symbol_list, 'mode': self.mode}
        self.user_data_save(symbol_1, symbol_2, symbol_3, symbol_4)
        self.base_signal.signal_symbol.emit(data)

    def data_verification(self, symbol_1, symbol_2, symbol_3, symbol_4) -> typing.Union[bool, list]:
        """数据校验"""
        if not symbol_1:
            self.message_box.info_message('“代码(1)”必须有值。', self)
            return False
        symbol_list = [symbol_1]
        if symbol_2:
            symbol_list.append(symbol_2)
        if symbol_3:
            symbol_list.append(symbol_3)
        if symbol_4:
            symbol_list.append(symbol_4)
        symbol_set = set(symbol_list)
        if len(symbol_set) != len(symbol_list):
            self.message_box.info_message('请确保已经已经输入的“代码”互不相同。', self)
            return False
        return symbol_list

    def msg(self) -> bool:
        try:
            self.config['config']['background_button']
        except KeyError:
            with open(self.user_data_path, "a") as f:
                user_data = (
                    '\n\n[config]\nbackground_button = false')
                f.write(user_data)
        self.config = ConfigObj(self.user_data_path, encoding='UTF8')
        background_button = self.config['config']['background_button']
        if background_button.lower() != 'true':
            msg = '请确认任务栏中，“数据”背景色是否与系统任务栏颜色一致？\n“确认”后将无法再修改背景色！'
        else:
            msg = '请确认代码是否填写正确？'
        message = QMessageBox(
            QMessageBox.Information, '确认框', msg, QMessageBox.Yes | QMessageBox.No | QMessageBox.Close,
            parent=self)
        message.button(QMessageBox.Yes).setText("确认")
        message.button(QMessageBox.No).setText("取消")
        message.button(QMessageBox.Close).setText("不在提示")
        message.exec()
        if message.clickedButton() == message.button(QMessageBox.No):
            return False
        if message.clickedButton() == message.button(QMessageBox.Close):
            self.msg_status = False
            self.base_signal.signal_msg_status.emit()
        return True

    def user_data_save(self, symbol, symbol_2, symbol_3, symbol_4):
        """保存在用户数据"""
        self.config['base']['symbol'] = symbol
        self.config['base']['symbol_2'] = symbol_2
        self.config['base']['symbol_3'] = symbol_3
        self.config['base']['symbol_4'] = symbol_4
        self.config['base']['mode'] = self.mode
        self.config['base']['interval'] = self.comboBox.currentText()
        self.config.write()
