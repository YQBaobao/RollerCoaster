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
        self.gridLayout = QtWidgets.QGridLayout(RollerCoaster)
        self.gridLayout.setContentsMargins(0, -1, 3, -1)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.label_value = QtWidgets.QLabel(RollerCoaster)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_value.sizePolicy().hasHeightForWidth())
        self.label_value.setSizePolicy(sizePolicy)
        self.label_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_value.setObjectName("label_value")
        self.gridLayout.addWidget(self.label_value, 0, 0, 1, 1)
        self.label_rate = QtWidgets.QLabel(RollerCoaster)
        self.label_rate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_rate.setObjectName("label_rate")
        self.gridLayout.addWidget(self.label_rate, 1, 0, 1, 1)

        self.retranslateUi(RollerCoaster)
        QtCore.QMetaObject.connectSlotsByName(RollerCoaster)

    def retranslateUi(self, RollerCoaster):
        _translate = QtCore.QCoreApplication.translate
        self.label_value.setText(_translate("RollerCoaster", "0000.00"))
        self.label_rate.setText(_translate("RollerCoaster", "-00.00%"))
