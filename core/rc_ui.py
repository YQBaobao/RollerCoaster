#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : rc_ui.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""

from PyQt5.QtCore import QMetaObject, QCoreApplication, QSize
from PyQt5.QtWidgets import QLabel, QGridLayout


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
