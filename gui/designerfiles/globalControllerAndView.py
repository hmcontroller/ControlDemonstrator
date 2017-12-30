# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'globalControllerAndView.ui'
#
# Created: Tue Nov 28 20:52:38 2017
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

class Ui_GlobalControllerAndView(object):
    def setupUi(self, GlobalControllerAndView):
        GlobalControllerAndView.setObjectName(_fromUtf8("GlobalControllerAndView"))
        GlobalControllerAndView.resize(1581, 73)
        GlobalControllerAndView.setMinimumSize(QtCore.QSize(0, 73))
        GlobalControllerAndView.setMaximumSize(QtCore.QSize(16777215, 73))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(GlobalControllerAndView)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.toolButtonSerialMonitor = QtGui.QToolButton(GlobalControllerAndView)
        self.toolButtonSerialMonitor.setText(_fromUtf8(""))
        self.toolButtonSerialMonitor.setObjectName(_fromUtf8("toolButtonSerialMonitor"))
        self.gridLayout.addWidget(self.toolButtonSerialMonitor, 1, 1, 1, 1)
        self.toolButtonSendPending = QtGui.QToolButton(GlobalControllerAndView)
        self.toolButtonSendPending.setObjectName(_fromUtf8("toolButtonSendPending"))
        self.gridLayout.addWidget(self.toolButtonSendPending, 0, 0, 1, 1)
        self.toolButtonCancelPending = QtGui.QToolButton(GlobalControllerAndView)
        self.toolButtonCancelPending.setObjectName(_fromUtf8("toolButtonCancelPending"))
        self.gridLayout.addWidget(self.toolButtonCancelPending, 1, 0, 1, 1)
        self.toolButtonRecordMode = QtGui.QToolButton(GlobalControllerAndView)
        self.toolButtonRecordMode.setObjectName(_fromUtf8("toolButtonRecordMode"))
        self.gridLayout.addWidget(self.toolButtonRecordMode, 1, 2, 1, 1)
        self.toolButtonPlay = QtGui.QToolButton(GlobalControllerAndView)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButtonPlay.sizePolicy().hasHeightForWidth())
        self.toolButtonPlay.setSizePolicy(sizePolicy)
        self.toolButtonPlay.setMaximumSize(QtCore.QSize(100, 100))
        self.toolButtonPlay.setObjectName(_fromUtf8("toolButtonPlay"))
        self.gridLayout.addWidget(self.toolButtonPlay, 0, 2, 1, 1)
        self.toolButtonDebugMode = QtGui.QToolButton(GlobalControllerAndView)
        self.toolButtonDebugMode.setObjectName(_fromUtf8("toolButtonDebugMode"))
        self.gridLayout.addWidget(self.toolButtonDebugMode, 0, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.messageTextEdit = QtGui.QTextEdit(GlobalControllerAndView)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.messageTextEdit.sizePolicy().hasHeightForWidth())
        self.messageTextEdit.setSizePolicy(sizePolicy)
        self.messageTextEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.messageTextEdit.setMaximumSize(QtCore.QSize(16777215, 200))
        self.messageTextEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.messageTextEdit.setObjectName(_fromUtf8("messageTextEdit"))
        self.horizontalLayout.addWidget(self.messageTextEdit)
        self.horizontalLayout_4.addLayout(self.horizontalLayout)

        self.retranslateUi(GlobalControllerAndView)
        QtCore.QMetaObject.connectSlotsByName(GlobalControllerAndView)

    def retranslateUi(self, GlobalControllerAndView):
        GlobalControllerAndView.setWindowTitle(_translate("GlobalControllerAndView", "Form", None))
        self.toolButtonSendPending.setText(_translate("GlobalControllerAndView", "...", None))
        self.toolButtonCancelPending.setText(_translate("GlobalControllerAndView", "...", None))
        self.toolButtonRecordMode.setText(_translate("GlobalControllerAndView", "...", None))
        self.toolButtonPlay.setText(_translate("GlobalControllerAndView", "...", None))
        self.toolButtonDebugMode.setText(_translate("GlobalControllerAndView", "...", None))

