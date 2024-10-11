#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : what_new.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import os

from PyQt5.QtWidgets import QWidget
from configobj import ConfigObj

from core import gitee_url, github_url
from temp import TEMP
from uis.rc_setting.what_new.what_new import Ui_WhatNew


class UiWhatNewQWidget(QWidget, Ui_WhatNew):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.init_ui()
        self.init_action()
        self.get_check_server()  # 获取url类型

    def init_ui(self):
        self.label.setOpenExternalLinks(True)
        self.label_2.setOpenExternalLinks(True)
        self.label_5.setOpenExternalLinks(True)
        self.label_7.setOpenExternalLinks(True)
        self.label_8.setOpenExternalLinks(True)

        self.user_data_path = os.path.join(TEMP, "user_data.ini")
        self.config = ConfigObj(self.user_data_path, encoding='UTF8')
        try:
            check_type = self.config['update']['check']
        except KeyError:
            check_type = 'gitee'
            with open(self.user_data_path, "a") as f:
                f.write('\n\n[update]\ncheck = gitee')
            self.config = ConfigObj(self.user_data_path, encoding='UTF8')  # 重新加载配置文件
        if check_type != 'gitee':
            self.radioButton.setChecked(True)
        else:
            self.radioButton_2.setChecked(True)

    def init_action(self):
        self.radioButton.toggled.connect(self.set_check_server)

    def get_check_server(self):
        if self.radioButton.isChecked():
            self.url = github_url
        if self.radioButton_2.isChecked():
            self.url = gitee_url
        print("Get Check Url: ", self.url)

    def set_check_server(self):
        if self.radioButton.isChecked():
            self.url = github_url
            self.config['update']['check'] = 'github'
            self.config.write()
        if self.radioButton_2.isChecked():
            self.url = gitee_url
            self.config['update']['check'] = 'gitee'
            self.config.write()
        print("Set Check Url: ", self.url)
