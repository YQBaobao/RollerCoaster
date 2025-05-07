#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : setting.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import sys

import aiohttp
from PyQt5.QtCore import Qt, QFile
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QSystemTrayIcon

from core import version
from core.rc_setting.background_color.background_color import UiBackgroundColorQWidget
from core.rc_setting.base.base import UiBaseQWidget
from core.rc_setting.futures.futures import UiFuturesQWidget
from core.rc_setting.home.home import UiHomeQWidget
from core.rc_setting.monitor_setting.monitor_setting import UiMonitorQWidget
from core.rc_setting.other.other import UiOtherQWidget
from core.rc_setting.shortcut_key.shortcut_key import UiShortcutKeyQWidget
from core.rc_setting.what_new.what_new import UiWhatNewQWidget
from uis.rc_setting.setting_ui import Ui_Settiing


def get_windows_version():
    version_info = sys.getwindowsversion()
    build = version_info.build
    return True if build >= 22000 else False


class UiSettingQWidget(QDialog, Ui_Settiing):
    type = Qt.UniqueConnection

    def __init__(
            self,
            base_signal,
            *args,
            parent=None,
            background_button=True,
            monitor_button=False,
            msg_status=True,
            msg_futures_status=True
    ):
        super().__init__(parent)
        self.setupUi(self)
        self.init_style()
        self.base_signal = base_signal
        self.base_tray: QSystemTrayIcon = args[0]
        self.background_button = background_button  # 背景色按钮状态
        self.monitor_button = monitor_button
        self.msg_status = msg_status
        self.msg_futures_status = msg_futures_status
        self.tags = ['0']  # 默认 0 版本

        self.stackedWidget.setCurrentIndex(0)
        self.init_ui()
        self.init_action_left_menu()
        self.init_action_widget()

    def init_style(self):
        qss = QFile(':/qss/qss/rc.qss')
        if qss.open(QFile.ReadOnly | QFile.Text):
            style_bytearray = qss.readAll()  # 类型为 QByteArray
            style = str(style_bytearray, encoding='UTF-8')
            self.setStyleSheet(style)
        qss.close()

    def init_ui(self):
        self.pushButton_background_color.setEnabled(self.background_button)
        self.pushButton_monitor.setEnabled(self.monitor_button)
        # 0
        self.ui_home = UiHomeQWidget(self)
        self.stackedWidget.addWidget(self.ui_home)  # 0
        # 1
        self.ui_base = UiBaseQWidget(self.base_signal, parent=self, msg_status=self.msg_status)
        self.stackedWidget.addWidget(self.ui_base)  # 1
        # 2
        self.ui_back_color = UiBackgroundColorQWidget(self.base_signal, self)
        self.stackedWidget.addWidget(self.ui_back_color)  # 2
        # 3
        self.ui_shortcut_key = UiShortcutKeyQWidget(self.base_signal, self)
        self.stackedWidget.addWidget(self.ui_shortcut_key)  # 3
        # 4
        self.ui_what_new = UiWhatNewQWidget(self)
        self.stackedWidget.addWidget(self.ui_what_new)  # 4
        # 5
        self.ui_monitor = UiMonitorQWidget(self.base_signal, self.base_tray, self)
        self.stackedWidget.addWidget(self.ui_monitor)  # 5

        # 6
        self.ui_futures = UiFuturesQWidget(self.base_signal, parent=self, msg_status=self.msg_futures_status)
        self.stackedWidget.addWidget(self.ui_futures)  # 6

        self.ui_other = UiOtherQWidget(self.base_signal, parent=self)
        self.stackedWidget.addWidget(self.ui_other)  # 7

    def init_action_left_menu(self):
        """菜单动作"""
        self.pushButton_home.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0), self.type)
        self.pushButton_base.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1), self.type)
        self.pushButton_background_color.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2), self.type)
        self.pushButton_shortcut_key.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3), self.type)
        self.pushButton_what_new.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4), self.type)
        self.pushButton_monitor.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5), self.type)
        self.pushButton_futures.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(6), self.type)
        self.pushButton_other.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(7), self.type)

    def init_action_widget(self):
        """部件动作"""
        self.ui_base.pushButton_accepted.clicked.connect(self.ui_base.setting_base, self.type)
        self.ui_futures.pushButton_accepted.clicked.connect(self.ui_futures.setting_futures, self.type)

        self.ui_back_color.pushButton_palette.clicked.connect(self.ui_back_color.get_palette, self.type)
        self.ui_back_color.pushButton_accepted_2.clicked.connect(self.ui_back_color.background_color, self.type)

        self.ui_shortcut_key.pb_open_setting.clicked.connect(self.ui_shortcut_key.key_open_setting, self.type)
        self.ui_shortcut_key.pb_show_data.clicked.connect(self.ui_shortcut_key.key_show_data, self.type)
        self.ui_shortcut_key.pb_red_green_switch.clicked.connect(self.ui_shortcut_key.key_red_green_switch, self.type)
        self.ui_shortcut_key.pb_boss_key.clicked.connect(self.ui_shortcut_key.key_boss_key, self.type)
        self.ui_shortcut_key.pb_accepted_3.clicked.connect(self.ui_shortcut_key.shortcut_key_save, self.type)

    async def check_update(self):
        url = self.ui_what_new.url
        print("Check: ", url)
        async with aiohttp.ClientSession() as session:
            if get_windows_version():
                # 兼容 win 11 或解决 aiohttp.client_exceptions.ClientConnectorCertificateError
                async with session.get(url, ssl=False) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.tags = [tag['name'] for tag in data]
                    else:
                        print("Check Update Request: ", await response.text())
            else:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.tags = [tag['name'] for tag in data]
                    else:
                        print("Check Update Request: ", await response.text())
        self.base_signal.signal_check_tags.emit(self.tags)
        self.set_check_update(self.tags)

    def set_check_update(self, tags):
        """判断，设置小红点"""
        if tags[0] <= version:
            return
        icon = QIcon()  # 小红点
        icon.addPixmap(QPixmap(":/rc/images/little_red_dot.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_what_new.setIcon(icon)

    def closeEvent(self, a0):
        self.base_signal.signal_setting_close.emit()
        super(UiSettingQWidget, self).closeEvent(a0)

""""
1.若开启了“基础信息、FC 信息”自启动，此时“背景色”将无法再改变。需要你先关闭对应功能的自启动，并重启软件方可修改“背景色”。
2.需要先开启“基础信息、FC 信息”中的任意一个后，才能开启“监控与提醒”的自启动。
"""