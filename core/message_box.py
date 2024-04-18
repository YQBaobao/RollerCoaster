#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : MQPush
@ File        : message_box.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox


class MessageBox(QObject):
    def __init__(self):
        super().__init__()

    @staticmethod
    def info_message(msg, parent=None):
        """消息提示"""
        message = QMessageBox(QMessageBox.Information, "提示", msg, QMessageBox.Yes, parent=parent)
        message.button(QMessageBox.Yes).setText('确定')
        message.exec()  # 模态显示
