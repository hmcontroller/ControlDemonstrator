# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'commandSettingsDialog.ui'
#
# Created: Wed May 17 20:27:53 2017
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

class Ui_CommandSettingsDialog(object):
    def setupUi(self, CommandSettingsDialog):
        CommandSettingsDialog.setObjectName(_fromUtf8("CommandSettingsDialog"))
        CommandSettingsDialog.resize(1067, 849)
        self.horizontalLayout = QtGui.QHBoxLayout(CommandSettingsDialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(CommandSettingsDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.toolButtonAddChannel = QtGui.QToolButton(CommandSettingsDialog)
        self.toolButtonAddChannel.setObjectName(_fromUtf8("toolButtonAddChannel"))
        self.horizontalLayout_3.addWidget(self.toolButtonAddChannel)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.tableWidget = QtGui.QTableWidget(CommandSettingsDialog)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.buttonBox = QtGui.QDialogButtonBox(CommandSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(CommandSettingsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CommandSettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CommandSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CommandSettingsDialog)

    def retranslateUi(self, CommandSettingsDialog):
        CommandSettingsDialog.setWindowTitle(_translate("CommandSettingsDialog", "Parametereinstellungen", None))
        self.label.setText(_translate("CommandSettingsDialog", "Parameter", None))
        self.toolButtonAddChannel.setText(_translate("CommandSettingsDialog", "...", None))

