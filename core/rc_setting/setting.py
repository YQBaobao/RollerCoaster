#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : setting.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from PyQt5.QtWidgets import QDialog, QGridLayout, QDesktopWidget

from core.rc_setting.background_color.background_color import UiBackgroundColorQWidget
from core.rc_setting.base.base import UiBaseQWidget
from core.rc_setting.home.home import UiHomeQWidget
from core.rc_setting.shortcut_key.shortcut_key import UiShortcutKeyQWidget
from core.rc_setting.what_new.what_new import UiWhatNewQWidget
from uis.rc_setting.setting_ui import Ui_Settiing


class UiSettingQWidget(QDialog, Ui_Settiing):

    def __init__(self, base_signal, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.base_signal = base_signal

        self.init_ui()
        self.init_action_left_menu()
        self.stackedWidget.setCurrentIndex(0)

    def init_ui(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))
        # 0
        self.ui_home = UiHomeQWidget(self)
        grid_layout = QGridLayout(self.ui_home)
        grid_layout.setObjectName("gridLayout_5")
        self.stackedWidget.addWidget(self.ui_home)  # 0
        # 1
        self.ui_base = UiBaseQWidget(self.base_signal, self)
        grid_layout = QGridLayout(self.ui_base)
        grid_layout.setObjectName("gridLayout_6")
        self.stackedWidget.addWidget(self.ui_base)  # 1
        # 2
        self.ui_background_color = UiBackgroundColorQWidget(self.base_signal, self)
        grid_layout = QGridLayout(self.ui_background_color)
        grid_layout.setObjectName("gridLayout_7")
        self.stackedWidget.addWidget(self.ui_background_color)  # 2
        # 3
        self.ui_shortcut_key = UiShortcutKeyQWidget(self)
        grid_layout = QGridLayout(self.ui_shortcut_key)
        grid_layout.setObjectName("gridLayout_8")
        self.stackedWidget.addWidget(self.ui_shortcut_key)  # 3
        # 4
        self.ui_what_new = UiWhatNewQWidget(self)
        grid_layout = QGridLayout(self.ui_what_new)
        grid_layout.setObjectName("gridLayout_9")
        self.stackedWidget.addWidget(self.ui_what_new)  # 4

    def init_action_left_menu(self):
        """动作"""
        self.pushButton_home.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_base.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_background_color.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pushButton_shortcut_key.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.pushButton_what_new.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
