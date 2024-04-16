#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : background_color.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from PyQt5.QtWidgets import QWidget, QColorDialog

from core.signals import BaseSignal
from uis.rc_setting.background_color.backgroud_color import Ui_BackgroundColor


class UiBackgroundColorQWidget(QWidget, Ui_BackgroundColor):
    dark = '#101010'
    light = '#eeeeee'
    dark_transparent = "#212221"
    light_transparent = '#c7c8c7'

    def __init__(self, base_signal: BaseSignal = None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.base_signal = base_signal

    def get_palette(self):
        c = QColorDialog.getColor()
        self.base_signal.signal_background_color.emit(c.name())

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
        self.base_signal.signal_background_color.emit(c)
