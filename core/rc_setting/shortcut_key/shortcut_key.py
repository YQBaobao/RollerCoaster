#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : shortcut_key.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QShortcut

from uis.rc_setting.shortcut_key.shortcut_key import Ui_ShortcutKey


class UiShortcutKeyQWidget(QWidget, Ui_ShortcutKey):
    def __init__(self, base_signal, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.signal = base_signal

    def shortcut_key(self):
        open_setting = self.pb_open_setting.text()
        show_data = self.pb_show_data.text()
        red_green_switch = self.pb_red_green_switch.text()
        boss_key = self.pb_boss_key.text()
        QShortcut(QKeySequence(open_setting), self.pb_open_setting, lambda: self.signal.signal_shortcut_key.emit(1))
        QShortcut(QKeySequence(show_data), self.pb_show_data, lambda: self.signal.signal_shortcut_key.emit(2))
        QShortcut(QKeySequence(red_green_switch), self.pb_red_green_switch,
                  lambda: self.signal.signal_shortcut_key.emit(3))
        QShortcut(QKeySequence(boss_key), self.pb_boss_key, lambda: self.signal.signal_shortcut_key.emit(4))

    # def keyPressEvent(self, event):
    #     print("按下：" + str(event.key()))
    #     if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_F:
    #         print("按下")
