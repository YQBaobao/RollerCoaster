# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster
@ File        : auto_run.py
@ Author      : yqbao
@ version     : V1.0.0
@ Description :
"""
import sys
import os
import winreg

def get_exe_path():
    """获取exe所在路径"""
    return sys.executable if getattr(sys, 'frozen', False) else os.path.realpath(__file__)


def is_auto_start_enabled(app_name):
    """检查状态"""
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(reg_key, app_name)
        winreg.CloseKey(reg_key)
        return value == get_exe_path()
    except FileNotFoundError:
        return False


def set_auto_start(app_name, exe_path):
    """设置开机自启"""
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(reg_key, app_name, 0, winreg.REG_SZ, exe_path)
    winreg.CloseKey(reg_key)


def disable_auto_start(app_name):
    """禁用开机自启"""
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteValue(reg_key, app_name)
        winreg.CloseKey(reg_key)
    except FileNotFoundError:
        pass  # 不存在时忽略
