#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : shortcut_key.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from PyQt5.QtWidgets import QWidget

from uis.rc_setting.shortcut_key.shortcut_key import Ui_ShortcutKey


class UiShortcutKeyQWidget(QWidget, Ui_ShortcutKey):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
