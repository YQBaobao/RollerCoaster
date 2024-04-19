#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : background_color.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import os

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QColorDialog
from configobj import ConfigObj

from core.signals import BaseSignal
from temp import TEMP
from uis.rc_setting.background_color.backgroud_color import Ui_BackgroundColor


class UiBackgroundColorQWidget(QWidget, Ui_BackgroundColor):
    dark = QColor(16, 16, 16)
    light = QColor(238, 238, 238)
    dark_transparent = QColor(33, 34, 33)
    light_transparent = QColor(199, 200, 199)

    def __init__(self, base_signal: BaseSignal = None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.base_signal = base_signal

    def get_palette(self):
        c = QColorDialog.getColor()
        self.pushButton_palette.setStyleSheet('background-color:{}'.format(c.name()))
        self.user_data_save(c)
        self.base_signal.signal_background_color.emit(c)

    def background_color(self):
        c = self.dark
        if self.radioButton.isChecked():
            c = self.light
        if self.radioButton_2.isChecked():
            c = self.dark
        if self.radioButton.isChecked() and self.checkBox.isChecked():
            c = self.light_transparent
        if self.radioButton_2.isChecked() and self.checkBox.isChecked():
            c = self.dark_transparent
        self.user_data_save(c)
        self.base_signal.signal_background_color.emit(c)

    @staticmethod
    def user_data_save(c: QColor):
        """保存在用户数据"""
        file_path = os.path.join(TEMP, "user_data.ini")
        config = ConfigObj(file_path, encoding='UTF8')
        config['background_color']['color'] = c.name()
        config.write()
