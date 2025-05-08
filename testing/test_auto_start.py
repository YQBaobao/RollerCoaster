# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster
@ File        : test_auto_start.py
@ Author      : yqbao
@ version     : V1.0.0
@ Description :
"""
import sys
import os
import winreg
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox

APP_NAME = "MyPyQtApp"

def get_exe_path():
    return sys.executable if getattr(sys, 'frozen', False) else os.path.realpath(__file__)

def is_auto_start_enabled(app_name):
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(reg_key, app_name)
        winreg.CloseKey(reg_key)
        return value == get_exe_path()
    except FileNotFoundError:
        return False

def set_auto_start(app_name, exe_path):
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(reg_key, app_name, 0, winreg.REG_SZ, exe_path)
    winreg.CloseKey(reg_key)

def disable_auto_start(app_name):
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteValue(reg_key, app_name)
        winreg.CloseKey(reg_key)
    except FileNotFoundError:
        pass  # 不存在时忽略

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("开机自启动控制")
        self.resize(300, 100)

        layout = QVBoxLayout()

        self.label = QLabel("请选择是否启用开机启动")
        self.checkbox = QCheckBox("开机自启动")

        # 检查状态初始化
        self.checkbox.setChecked(is_auto_start_enabled(APP_NAME))

        self.checkbox.stateChanged.connect(self.toggle_auto_start)

        layout.addWidget(self.label)
        layout.addWidget(self.checkbox)

        self.setLayout(layout)

    def toggle_auto_start(self, state):
        if self.checkbox.isChecked():
            set_auto_start(APP_NAME, get_exe_path())
            self.label.setText("开机启动已启用")
        else:
            disable_auto_start(APP_NAME)
            self.label.setText("开机启动已关闭")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
