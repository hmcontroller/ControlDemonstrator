# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'valuesToInitialValuesDialog.ui'
#
# Created: Fri May 26 21:16:23 2017
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_valuesToInitialValuesDialog(object):
    def setupUi(self, valuesToInitialValuesDialog):
        valuesToInitialValuesDialog.setObjectName(_fromUtf8("valuesToInitialValuesDialog"))
        valuesToInitialValuesDialog.resize(1067, 849)
        self.horizontalLayout = QtGui.QHBoxLayout(valuesToInitialValuesDialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(valuesToInitialValuesDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.pushButtonSelectAll = QtGui.QPushButton(valuesToInitialValuesDialog)
        self.pushButtonSelectAll.setObjectName(_fromUtf8("pushButtonSelectAll"))
        self.horizontalLayout_3.addWidget(self.pushButtonSelectAll)
        self.pushButtonDeselectAll = QtGui.QPushButton(valuesToInitialValuesDialog)
        self.pushButtonDeselectAll.setObjectName(_fromUtf8("pushButtonDeselectAll"))
        self.horizontalLayout_3.addWidget(self.pushButtonDeselectAll)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.tableWidget = QtGui.QTableWidget(valuesToInitialValuesDialog)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.buttonBox = QtGui.QDialogButtonBox(valuesToInitialValuesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(valuesToInitialValuesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), valuesToInitialValuesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), valuesToInitialValuesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(valuesToInitialValuesDialog)

    def retranslateUi(self, valuesToInitialValuesDialog):
        valuesToInitialValuesDialog.setWindowTitle(_translate("valuesToInitialValuesDialog", "Startwerte übernehmen", None))
        self.label.setText(_translate("valuesToInitialValuesDialog", "Startwerte übernehmen", None))
        self.pushButtonSelectAll.setText(_translate("valuesToInitialValuesDialog", "alle", None))
        self.pushButtonDeselectAll.setText(_translate("valuesToInitialValuesDialog", "keine", None))

