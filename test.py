#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster
@ File        : main.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description :
"""
import sys

import win32gui
from PyQt5.QtCore import Qt, QMetaObject, QCoreApplication, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout


class UiRollerCoaster(object):
    def setup_ui(self, roller_coaster):
        if not roller_coaster.objectName():
            roller_coaster.setObjectName(u"RollerCoaster")
        roller_coaster.resize(203, 69)
        roller_coaster.setMinimumSize(QSize(170, 50))
        self.gridLayout = QGridLayout(roller_coaster)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_value1 = QLabel(roller_coaster)
        self.label_value1.setObjectName(u"label_value1")
        self.gridLayout.addWidget(self.label_value1, 0, 0, 1, 1)

        self.label_value2 = QLabel(roller_coaster)
        self.label_value2.setObjectName(u"label_value2")
        self.gridLayout.addWidget(self.label_value2, 0, 1, 1, 1)

        self.label_value3 = QLabel(roller_coaster)
        self.label_value3.setObjectName(u"label_value3")
        self.gridLayout.addWidget(self.label_value3, 0, 2, 1, 1)

        self.label_rate1 = QLabel(roller_coaster)
        self.label_rate1.setObjectName(u"label_rate1")
        self.gridLayout.addWidget(self.label_rate1, 1, 0, 1, 1)

        self.label_rate2 = QLabel(roller_coaster)
        self.label_rate2.setObjectName(u"label_rate2")
        self.gridLayout.addWidget(self.label_rate2, 1, 1, 1, 1)

        self.label_rate3 = QLabel(roller_coaster)
        self.label_rate3.setObjectName(u"label_rate3")
        self.gridLayout.addWidget(self.label_rate3, 1, 2, 1, 1)

        self.re_translate_ui(roller_coaster)
        QMetaObject.connectSlotsByName(roller_coaster)

    def re_translate_ui(self, roller_coaster):
        roller_coaster.setWindowTitle(QCoreApplication.translate("RollerCoaster", u"Form", None))
        self.label_value1.setText(QCoreApplication.translate("RollerCoaster", u"321.22", None))
        self.label_value2.setText(QCoreApplication.translate("RollerCoaster", u"321.22", None))
        self.label_value3.setText(QCoreApplication.translate("RollerCoaster", u"321.22", None))
        self.label_rate1.setText(QCoreApplication.translate("RollerCoaster", u"32.22%", None))
        self.label_rate2.setText(QCoreApplication.translate("RollerCoaster", u"32.22%", None))
        self.label_rate3.setText(QCoreApplication.translate("RollerCoaster", u"32.22%", None))


class MyApp(QWidget, UiRollerCoaster):
    def __init__(self):
        super().__init__()
        self.setup_ui(self)
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
        self.setWindowFlags(Qt.FramelessWindowHint)  # 窗口无边框
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)  # 窗口置顶，无边框
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)  # 窗口置顶，无边框，在任务栏不显示图标
        # self.setStyleSheet("QLabel{color: white;}")

        self.init_ui()

    def init_ui(self):
        m_h_taskbar = win32gui.FindWindow("Shell_TrayWnd", None)  # 任务栏“Shell_TaryWnd”的窗口句柄
        m_h_bar = win32gui.FindWindowEx(m_h_taskbar, 0, "ReBarWindow32", None)  # 子窗口“ReBarWindow32”的窗口句柄
        m_h_min = win32gui.FindWindowEx(m_h_bar, 0, "MSTaskSwWClass", None)  # 子窗口“MSTaskSwWClass”的窗口句柄
        b = win32gui.GetWindowRect(m_h_bar)  # 获取m_hBar窗口尺寸b为[左，上，右，下]的数组
        win32gui.MoveWindow(m_h_min, 0, 0, b[2] - b[0] - 160, b[3] - b[1], True)  # 调整m_hMin的窗口大小，为我们的程序预留出位置

        self.setGeometry(b[2] - b[0] - 160, 0, 160, b[3] - b[1])  # 调整我们自己的窗口到预留位置的大小
        win32gui.SetParent(int(self.winId()), m_h_bar)  # 将我们自己的窗口设置为m_hBar的子窗口

        self.show()  # 显示窗口


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
