# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster
@ File        : test_zoom.py
@ Author      : yqbao
@ version     : V1.0.0
@ Description :
"""
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout


def main():
    # 高 DPI 设置 —— 必须在 QApplication 之前
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    # Qt 5.14+ 可用 PassThrough 让缩放值不四舍五入（125% 就是 1.25）
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    # 创建应用
    app = QApplication(sys.argv)
    win = QWidget()
    win.setWindowTitle("High DPI Demo")

    label = QLabel("在不同 DPI 的屏幕上拖动窗口看看字体和布局变化")
    label.setWordWrap(True)

    btn1 = QPushButton("按钮 1")
    btn2 = QPushButton("按钮 2")

    layout = QVBoxLayout()
    layout.addWidget(label)
    layout.addWidget(btn1)
    layout.addWidget(btn2)
    layout.addStretch()

    win.setLayout(layout)
    win.resize(400, 200)
    win.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
