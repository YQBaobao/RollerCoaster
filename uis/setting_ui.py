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
        Settiing.resize(240, 64)
        Settiing.setMinimumSize(QtCore.QSize(240, 64))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/rc/images/microscope.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Settiing.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Settiing)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Settiing)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Settiing)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Settiing)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(Settiing)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Settiing)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 2, 2, 1)

        self.retranslateUi(Settiing)
        self.comboBox.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Settiing)

    def retranslateUi(self, Settiing):
        _translate = QtCore.QCoreApplication.translate
        Settiing.setWindowTitle(_translate("Settiing", "Settiing"))
        self.label.setText(_translate("Settiing", "完整代码"))
        self.lineEdit.setText(_translate("Settiing", "SZ002594"))
        self.label_2.setText(_translate("Settiing", "获取延迟"))
        self.comboBox.setItemText(0, _translate("Settiing", "1秒"))
        self.comboBox.setItemText(1, _translate("Settiing", "2秒"))
        self.comboBox.setItemText(2, _translate("Settiing", "3秒"))
        self.comboBox.setItemText(3, _translate("Settiing", "5秒"))
        self.comboBox.setItemText(4, _translate("Settiing", "10秒"))
        self.pushButton.setText(_translate("Settiing", "确定"))
