#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : test_2.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
# -*- coding: utf-8 -*-


import sys

from PyQt5.QtCore import Qt, QMetaObject, QCoreApplication, QSize, QPoint
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout


class UiRollerCoaster(object):
    def setup_ui(self, roller_coaster):
        if not roller_coaster.objectName():
            roller_coaster.setObjectName(u"RollerCoaster")
        roller_coaster.resize(300, 300)
        # roller_coaster.setMinimumSize(QSize(170, 50))
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


class MyWindow(QWidget, UiRollerCoaster):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui(self)
        self.setStyleSheet("QLabel{color: white;}")

        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)  # 窗口置顶，无边框，在任务栏不显示图标

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MyWindow()
    mainWindow.show()
    sys.exit(app.exec_())
