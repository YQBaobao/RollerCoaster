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
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox

from lib.auto_run import is_auto_start_enabled, set_auto_start, get_exe_path, disable_auto_start

APP_NAME = "MyPyQtApp"


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
