# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rc_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RollerCoaster(object):
    def setupUi(self, RollerCoaster):
        RollerCoaster.setObjectName("RollerCoaster")
        RollerCoaster.resize(94, 48)
        self.gridLayout = QtWidgets.QGridLayout(RollerCoaster)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(RollerCoaster)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_rate = QtWidgets.QLabel(RollerCoaster)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_rate.sizePolicy().hasHeightForWidth())
        self.label_rate.setSizePolicy(sizePolicy)
        self.label_rate.setObjectName("label_rate")
        self.gridLayout.addWidget(self.label_rate, 1, 1, 1, 1)
        self.label_value = QtWidgets.QLabel(RollerCoaster)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_value.sizePolicy().hasHeightForWidth())
        self.label_value.setSizePolicy(sizePolicy)
        self.label_value.setObjectName("label_value")
        self.gridLayout.addWidget(self.label_value, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(RollerCoaster)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.retranslateUi(RollerCoaster)
        QtCore.QMetaObject.connectSlotsByName(RollerCoaster)

    def retranslateUi(self, RollerCoaster):
        _translate = QtCore.QCoreApplication.translate
        RollerCoaster.setWindowTitle(_translate("RollerCoaster", "Form"))
        self.label_2.setText(_translate("RollerCoaster", "C:"))
        self.label_rate.setText(_translate("RollerCoaster", "32.22%"))
        self.label_value.setText(_translate("RollerCoaster", "321.22"))
        self.label.setText(_translate("RollerCoaster", "P:"))
