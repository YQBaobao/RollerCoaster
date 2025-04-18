# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Settiing(object):
    def setupUi(self, Settiing):
        Settiing.setObjectName("Settiing")
        Settiing.resize(543, 257)
        Settiing.setMinimumSize(QtCore.QSize(543, 257))
        Settiing.setMaximumSize(QtCore.QSize(543, 257))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/rc/images/microscope.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Settiing.setWindowIcon(icon)
        self._2 = QtWidgets.QGridLayout(Settiing)
        self._2.setObjectName("_2")
        self.stackedWidget = QtWidgets.QStackedWidget(Settiing)
        self.stackedWidget.setMinimumSize(QtCore.QSize(385, 0))
        self.stackedWidget.setMaximumSize(QtCore.QSize(385, 16777215))
        self.stackedWidget.setObjectName("stackedWidget")
        self._2.addWidget(self.stackedWidget, 0, 1, 2, 1)
        self.scrollArea = QtWidgets.QScrollArea(Settiing)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 134, 192))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_shortcut_key = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_shortcut_key.setCheckable(True)
        self.pushButton_shortcut_key.setAutoExclusive(True)
        self.pushButton_shortcut_key.setObjectName("pushButton_shortcut_key")
        self.buttonGroup = QtWidgets.QButtonGroup(Settiing)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.pushButton_shortcut_key)
        self.gridLayout_3.addWidget(self.pushButton_shortcut_key, 5, 0, 1, 1)
        self.pushButton_home = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_home.setCheckable(True)
        self.pushButton_home.setChecked(True)
        self.pushButton_home.setAutoExclusive(True)
        self.pushButton_home.setObjectName("pushButton_home")
        self.buttonGroup.addButton(self.pushButton_home)
        self.gridLayout_3.addWidget(self.pushButton_home, 0, 0, 1, 1)
        self.pushButton_base = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_base.setCheckable(True)
        self.pushButton_base.setAutoExclusive(True)
        self.pushButton_base.setObjectName("pushButton_base")
        self.buttonGroup.addButton(self.pushButton_base)
        self.gridLayout_3.addWidget(self.pushButton_base, 1, 0, 1, 1)
        self.pushButton_monitor = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_monitor.setCheckable(True)
        self.pushButton_monitor.setAutoExclusive(True)
        self.pushButton_monitor.setObjectName("pushButton_monitor")
        self.buttonGroup.addButton(self.pushButton_monitor)
        self.gridLayout_3.addWidget(self.pushButton_monitor, 3, 0, 1, 1)
        self.pushButton_background_color = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_background_color.setCheckable(True)
        self.pushButton_background_color.setAutoExclusive(True)
        self.pushButton_background_color.setObjectName("pushButton_background_color")
        self.buttonGroup.addButton(self.pushButton_background_color)
        self.gridLayout_3.addWidget(self.pushButton_background_color, 4, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 6, 0, 1, 1)
        self.pushButton_futures = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_futures.setCheckable(True)
        self.pushButton_futures.setAutoExclusive(True)
        self.pushButton_futures.setObjectName("pushButton_futures")
        self.buttonGroup.addButton(self.pushButton_futures)
        self.gridLayout_3.addWidget(self.pushButton_futures, 2, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self._2.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(Settiing)
        self.frame.setObjectName("frame")
        self.hboxlayout = QtWidgets.QHBoxLayout(self.frame)
        self.hboxlayout.setObjectName("hboxlayout")
        self.pushButton_what_new = QtWidgets.QPushButton(self.frame)
        self.pushButton_what_new.setCheckable(True)
        self.pushButton_what_new.setAutoExclusive(True)
        self.pushButton_what_new.setObjectName("pushButton_what_new")
        self.buttonGroup.addButton(self.pushButton_what_new)
        self.hboxlayout.addWidget(self.pushButton_what_new)
        self._2.addWidget(self.frame, 1, 0, 1, 1)

        self.retranslateUi(Settiing)
        QtCore.QMetaObject.connectSlotsByName(Settiing)

    def retranslateUi(self, Settiing):
        _translate = QtCore.QCoreApplication.translate
        Settiing.setWindowTitle(_translate("Settiing", "RollerCoaster"))
        self.pushButton_shortcut_key.setText(_translate("Settiing", "快捷键设置"))
        self.pushButton_home.setText(_translate("Settiing", "首页"))
        self.pushButton_base.setText(_translate("Settiing", "基础信息"))
        self.pushButton_monitor.setText(_translate("Settiing", "监控与提醒"))
        self.pushButton_background_color.setText(_translate("Settiing", "背景色"))
        self.pushButton_futures.setText(_translate("Settiing", "FC信息"))
        self.pushButton_what_new.setText(_translate("Settiing", "新功能？"))
