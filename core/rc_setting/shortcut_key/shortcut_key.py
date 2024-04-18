#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : shortcut_key.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget
from configobj import ConfigObj

from core.message_box import MessageBox
from temp import TEMP
from uis.rc_setting.shortcut_key.shortcut_key import Ui_ShortcutKey


class UiShortcutKeyQWidget(QWidget, Ui_ShortcutKey):
    def __init__(self, base_signal, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.signal = base_signal

        self.button = 0
        self.key = []

        self.init_ui()

    def init_ui(self):
        file_path = os.path.join(TEMP, "user_data.ini")
        self.config = ConfigObj(file_path, encoding='UTF8')
        self.pb_open_setting.setText(self.shortcut_key_show(self.config['shortcut_key']['open_setting']))
        self.pb_show_data.setText(self.shortcut_key_show(self.config['shortcut_key']['show_data']))
        self.pb_red_green_switch.setText(self.shortcut_key_show(self.config['shortcut_key']['red_green_switch']))
        self.pb_boss_key.setText(self.shortcut_key_show(self.config['shortcut_key']['boss_key']))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        print("按下：" + str(event.key()), event.text())
        if self.button == 1:
            key = self.shortcut_key_unformat(self.key, event)
            key = self.set_shortcut_key(key)
            self.pb_open_setting.setText('+'.join(key))

        if self.button == 2:
            key = self.shortcut_key_unformat(self.key, event)
            key = self.set_shortcut_key(key)
            self.pb_show_data.setText('+'.join(key))

        if self.button == 3:
            key = self.shortcut_key_unformat(self.key, event)
            key = self.set_shortcut_key(key)
            self.pb_red_green_switch.setText('+'.join(key))

        if self.button == 4:
            key = self.shortcut_key_unformat(self.key, event)
            key = self.set_shortcut_key(key)
            self.pb_boss_key.setText('+'.join(key))

    def key_open_setting(self):
        """更新快捷键"""
        self.button = 1
        self.key = []
        self.pb_open_setting.setText('')

    def key_show_data(self):
        self.button = 2
        self.key = []
        self.pb_show_data.setText('')

    def key_red_green_switch(self):
        self.button = 3
        self.key = []
        self.pb_red_green_switch.setText('')

    def key_boss_key(self):
        self.button = 4
        self.key = []
        self.pb_boss_key.setText('')

    def shortcut_key_save(self):
        """保存在用户数据"""
        open_setting = self.shortcut_key_format(self.pb_open_setting.text())
        show_data = self.shortcut_key_format(self.pb_show_data.text())
        red_green_switch = self.shortcut_key_format(self.pb_red_green_switch.text())
        boss_key = self.shortcut_key_format(self.pb_boss_key.text())

        self.config['shortcut_key']['open_setting'] = open_setting
        self.config['shortcut_key']['show_data'] = show_data
        self.config['shortcut_key']['red_green_switch'] = red_green_switch
        self.config['shortcut_key']['boss_key'] = boss_key
        self.config.write()

        self.signal.signal_shortcut_key_update.emit()
        self.message_box = MessageBox()
        self.message_box.info_message('设置已更新。', self)

    @staticmethod
    def set_shortcut_key(key):
        for i, v in enumerate(key):
            x = v.lower()
            if x == "control":
                key[i] = "ctrl"
            if x == "super":
                key[i] = "win"
        return key

    @staticmethod
    def shortcut_key_format(key):
        key = key.split('+')
        for i, v in enumerate(key):
            x = v.lower()
            if x == "ctrl":
                key[i] = "control"
            elif x == "win":
                key[i] = "super"
            else:
                key[i] = x
        return '+'.join(key)

    @staticmethod
    def shortcut_key_show(shortcut_key=''):
        key = shortcut_key.split('+')
        for i, v in enumerate(key):
            x = v.lower()
            if x == "control":
                key[i] = "ctrl"
            elif x == "super":
                key[i] = "win"
            else:
                key[i] = x
        return '+'.join(key)

    @staticmethod
    def shortcut_key_unformat(key: list, event: QKeyEvent):
        # TODO 设置组合键时，必须按下松开，而不是连续按,这有点反人类
        if event.modifiers() == Qt.ControlModifier:
            key.append('control')
            key = list(filter(lambda x: x and x.strip(), key))
            return key
        if event.modifiers() == Qt.ShiftModifier:
            key.append('shift')
            key = list(filter(lambda x: x and x.strip(), key))
            return key
        if event.modifiers() == Qt.AltModifier:
            key.append('alt')
            key = list(filter(lambda x: x and x.strip(), key))
            return key
        if event.modifiers() == Qt.Key_Meta:
            key.append('super')
            key = list(filter(lambda x: x and x.strip(), key))
            return key
        if key:
            key.append(event.text())
            key = list(filter(lambda x: x and x.strip(), key))
            return key
        return event.text()
