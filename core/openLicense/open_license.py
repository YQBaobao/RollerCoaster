#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster
@ File        : open_license.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description :
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDesktopWidget

from core.openLicense.about_qt import UiAboutQtQWidget
from uis.openLicense.open_license import Ui_OpenLicense


class UiOpenLicenseQWidget(QDialog, Ui_OpenLicense):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

        self.pushButtonAbout.clicked.connect(self.about_qt)

    def about_qt(self):
        about_qt_dialog = UiAboutQtQWidget(self)
        about_qt_dialog.setWindowFlag(Qt.WindowContextHelpButtonHint, on=False)  # 取消帮助按钮
        about_qt_dialog.exec()
