# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serialMonitor.ui'
#
# Created: Thu Jan 04 13:34:30 2018
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

class Ui_SerialMonitor(object):
    def setupUi(self, SerialMonitor):
        SerialMonitor.setObjectName(_fromUtf8("SerialMonitor"))
        SerialMonitor.resize(1245, 469)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SerialMonitor.sizePolicy().hasHeightForWidth())
        SerialMonitor.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(SerialMonitor)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.plainTextEdit = QtGui.QPlainTextEdit(SerialMonitor)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEditCommand = QtGui.QLineEdit(SerialMonitor)
        self.lineEditCommand.setObjectName(_fromUtf8("lineEditCommand"))
        self.horizontalLayout.addWidget(self.lineEditCommand)
        self.pushButtonSend = QtGui.QPushButton(SerialMonitor)
        self.pushButtonSend.setObjectName(_fromUtf8("pushButtonSend"))
        self.horizontalLayout.addWidget(self.pushButtonSend)
        self.toolButtonPlay = QtGui.QToolButton(SerialMonitor)
        self.toolButtonPlay.setObjectName(_fromUtf8("toolButtonPlay"))
        self.horizontalLayout.addWidget(self.toolButtonPlay)
        self.checkBoxAutoScroll = QtGui.QCheckBox(SerialMonitor)
        self.checkBoxAutoScroll.setObjectName(_fromUtf8("checkBoxAutoScroll"))
        self.horizontalLayout.addWidget(self.checkBoxAutoScroll)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(SerialMonitor)
        QtCore.QMetaObject.connectSlotsByName(SerialMonitor)

    def retranslateUi(self, SerialMonitor):
        SerialMonitor.setWindowTitle(_translate("SerialMonitor", "Kanaleinstellungen", None))
        self.pushButtonSend.setText(_translate("SerialMonitor", "Send", None))
        self.toolButtonPlay.setText(_translate("SerialMonitor", "...", None))
        self.checkBoxAutoScroll.setText(_translate("SerialMonitor", "Autoscroll", None))

