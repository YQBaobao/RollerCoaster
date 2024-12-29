#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : signals.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from PyQt5.QtCore import QObject, pyqtSignal


class BaseSignal(QObject):
    signal_symbol = pyqtSignal(dict)  # 基础信号
    signal_background_color = pyqtSignal(object)  # 背景色信号
    signal_shortcut_key = pyqtSignal(int)  # 快捷键
    signal_shortcut_key_update = pyqtSignal()

    signal_setting_close = pyqtSignal()  # 设置页面关闭信号
    signal_msg_status = pyqtSignal()

    signal_check_tags = pyqtSignal(list)  # 标签版本信息

    signal_monitor_data = pyqtSignal(list)  # 监控数据
    signal_monitor_msg = pyqtSignal(list)
