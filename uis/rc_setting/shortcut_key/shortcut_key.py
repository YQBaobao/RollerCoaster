# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shortcut_key.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ShortcutKey(object):
    def setupUi(self, ShortcutKey):
        ShortcutKey.setObjectName("ShortcutKey")
        ShortcutKey.resize(367, 187)
        self.gridLayout = QtWidgets.QGridLayout(ShortcutKey)
        self.gridLayout.setObjectName("gridLayout")
        self.pb_show_data = QtWidgets.QPushButton(ShortcutKey)
        self.pb_show_data.setObjectName("pb_show_data")
        self.gridLayout.addWidget(self.pb_show_data, 1, 1, 1, 2)
        self.pb_open_setting = QtWidgets.QPushButton(ShortcutKey)
        self.pb_open_setting.setObjectName("pb_open_setting")
        self.gridLayout.addWidget(self.pb_open_setting, 0, 1, 1, 2)
        self.label_10 = QtWidgets.QLabel(ShortcutKey)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(ShortcutKey)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(ShortcutKey)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.pb_boss_key = QtWidgets.QPushButton(ShortcutKey)
        self.pb_boss_key.setObjectName("pb_boss_key")
        self.gridLayout.addWidget(self.pb_boss_key, 3, 1, 1, 2)
        self.pb_red_green_switch = QtWidgets.QPushButton(ShortcutKey)
        self.pb_red_green_switch.setObjectName("pb_red_green_switch")
        self.gridLayout.addWidget(self.pb_red_green_switch, 2, 1, 1, 2)
        self.label_9 = QtWidgets.QLabel(ShortcutKey)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(ShortcutKey)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(ShortcutKey)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 1, 1, 1)
        self.pb_accepted_3 = QtWidgets.QPushButton(ShortcutKey)
        self.pb_accepted_3.setObjectName("pb_accepted_3")
        self.gridLayout.addWidget(self.pb_accepted_3, 4, 2, 1, 1)

        self.retranslateUi(ShortcutKey)
        QtCore.QMetaObject.connectSlotsByName(ShortcutKey)

    def retranslateUi(self, ShortcutKey):
        _translate = QtCore.QCoreApplication.translate
        ShortcutKey.setWindowTitle(_translate("ShortcutKey", "Form"))
        self.label_10.setText(_translate("ShortcutKey", "显示/隐藏任务栏数据"))
        self.label_11.setText(_translate("ShortcutKey", "老板键"))
        self.label.setText(_translate("ShortcutKey", "绿变红（滑稽）"))
        self.label_9.setText(_translate("ShortcutKey", "打开/关闭设置"))
        self.pb_accepted_3.setText(_translate("ShortcutKey", "确认"))
