# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'channelSettingsDialog.ui'
#
# Created: Sat May 13 15:16:13 2017
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

class Ui_ChannelSettingsDialog(object):
    def setupUi(self, ChannelSettingsDialog):
        ChannelSettingsDialog.setObjectName(_fromUtf8("ChannelSettingsDialog"))
        ChannelSettingsDialog.resize(503, 849)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ChannelSettingsDialog.sizePolicy().hasHeightForWidth())
        ChannelSettingsDialog.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(ChannelSettingsDialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(ChannelSettingsDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.toolButtonAddChannel = QtGui.QToolButton(ChannelSettingsDialog)
        self.toolButtonAddChannel.setObjectName(_fromUtf8("toolButtonAddChannel"))
        self.horizontalLayout_3.addWidget(self.toolButtonAddChannel)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.tableWidget = QtGui.QTableWidget(ChannelSettingsDialog)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.buttonBox = QtGui.QDialogButtonBox(ChannelSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(ChannelSettingsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ChannelSettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ChannelSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ChannelSettingsDialog)

    def retranslateUi(self, ChannelSettingsDialog):
        ChannelSettingsDialog.setWindowTitle(_translate("ChannelSettingsDialog", "Kanaleinstellungen", None))
        self.label.setText(_translate("ChannelSettingsDialog", "Kanäle", None))
        self.toolButtonAddChannel.setText(_translate("ChannelSettingsDialog", "...", None))

