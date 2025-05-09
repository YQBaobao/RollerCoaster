# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster
@ File        : other.py
@ Author      : yqbao
@ version     : V1.0.0
@ Description :
"""
import os

from PyQt5.QtWidgets import QWidget
from configobj import ConfigObj

from core import APP_NAME
from lib.auto_run import is_auto_start_enabled, get_exe_path, set_auto_start, disable_auto_start
from temp import TEMP
from uis.rc_setting.other.other import Ui_Other


class UiOtherQWidget(QWidget, Ui_Other):
    def __init__(self, base_signal, parent=None, ):
        super().__init__(parent)
        self.setupUi(self)
        self.base_signal = base_signal

        self.init_ui()

        self.checkBox_sys.toggled.connect(self.sys_toggled)
        self.checkBox_polling.toggled.connect(self.polling_toggled)
        self.checkBox_futures.toggled.connect(self.futures_toggled)
        self.checkBox_monitor.toggled.connect(self.monitor_toggled)

    def init_ui(self):
        """状态初始化"""
        self.checkBox_sys.setChecked(is_auto_start_enabled(APP_NAME))  # 检查状态初始化
        self.checkBox_monitor.setEnabled(False)

        self.user_data_path = os.path.join(TEMP, "user_data.ini")
        self.config = ConfigObj(self.user_data_path, encoding='UTF8')
        setting = self.config['setting']
        self.checkBox_polling.setChecked(True if setting['polling'].lower() == 'true' else False)
        self.checkBox_futures.setChecked(True if setting['futures'].lower() == 'true' else False)
        self.checkBox_monitor.setChecked(True if setting['monitor'].lower() == 'true' else False)

        self.checkBox_polling.toggled.connect(self.checkbox_toggled)
        # self.checkBox_futures.toggled.connect(self.checkbox_toggled)

    def sys_toggled(self, checked):
        """软件开机自启"""
        if checked:
            set_auto_start(APP_NAME, get_exe_path())
        else:
            disable_auto_start(APP_NAME)
        self.user_data_save('system', checked)

    def polling_toggled(self, checked):
        self.user_data_save('polling', checked)

    def futures_toggled(self, checked):
        self.user_data_save('futures', checked)

    def monitor_toggled(self, checked):
        self.user_data_save('monitor', checked)

    def checkbox_toggled(self):
        if self.checkBox_polling.isChecked():
            self.checkBox_monitor.setEnabled(True)
        else:
            self.checkBox_monitor.setChecked(False)
            self.checkBox_monitor.setEnabled(False)

    def user_data_save(self, key, value):
        """保存在用户数据"""
        self.config['setting'][key] = value
        self.config.write()
