#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtLoginRegistration 
@ File        : message_box.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 基础公共方法类
"""

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox


class MessageBox(QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    @staticmethod
    def info_message(msg):
        """公共的消息提示"""
        message = QMessageBox(QMessageBox.Information, "提示", msg, QMessageBox.Yes)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/rc/images/microscope.ico"), QIcon.Normal, QIcon.Off)
        message.setWindowIcon(icon)
        message.button(QMessageBox.Yes).setText('确定')
        message.exec()  # 模态显示
