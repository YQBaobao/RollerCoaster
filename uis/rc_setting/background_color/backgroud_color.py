# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'backgroud_color.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BackgroundColor(object):
    def setupUi(self, BackgroundColor):
        BackgroundColor.setObjectName("BackgroundColor")
        BackgroundColor.resize(356, 169)
        self.gridLayout = QtWidgets.QGridLayout(BackgroundColor)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(BackgroundColor)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 75))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout_3.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout_3.addWidget(self.radioButton_2)
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_3.addWidget(self.checkBox)
        self.pushButton_accepted_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_accepted_2.setObjectName("pushButton_accepted_2")
        self.verticalLayout_3.addWidget(self.pushButton_accepted_2)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 3, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(BackgroundColor)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.pushButton_palette = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_palette.sizePolicy().hasHeightForWidth())
        self.pushButton_palette.setSizePolicy(sizePolicy)
        self.pushButton_palette.setObjectName("pushButton_palette")
        self.gridLayout_7.addWidget(self.pushButton_palette, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 0, 1, 3, 1)

        self.retranslateUi(BackgroundColor)
        QtCore.QMetaObject.connectSlotsByName(BackgroundColor)

    def retranslateUi(self, BackgroundColor):
        _translate = QtCore.QCoreApplication.translate
        BackgroundColor.setWindowTitle(_translate("BackgroundColor", "Form"))
        self.groupBox.setTitle(_translate("BackgroundColor", "您的 Windows 模式"))
        self.radioButton.setText(_translate("BackgroundColor", "浅色"))
        self.radioButton_2.setText(_translate("BackgroundColor", "深色"))
        self.checkBox.setText(_translate("BackgroundColor", "是否开启透明效果"))
        self.pushButton_accepted_2.setText(_translate("BackgroundColor", "确定"))
        self.groupBox_3.setTitle(_translate("BackgroundColor", "自定义背景色"))
        self.pushButton_palette.setText(_translate("BackgroundColor", "调色板"))
