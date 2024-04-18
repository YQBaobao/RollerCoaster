#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster
@ File        : about_qt.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description :
"""
from PyQt5.QtWidgets import QDialog

from uis.openLicense.about import Ui_AboutQt


class UiAboutQtQWidget(QDialog, Ui_AboutQt):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.pushButtonAbout.clicked.connect(lambda: self.close())
