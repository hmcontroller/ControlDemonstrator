# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'globalControllerAndView.ui'
#
# Created: Sun Apr 09 09:22:35 2017
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
        GlobalControllerAndView.resize(1554, 57)
        GlobalControllerAndView.setMaximumSize(QtCore.QSize(16777215, 57))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(GlobalControllerAndView)
        self.horizontalLayout_6.setMargin(0)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.pendingGroupBox = QtGui.QGroupBox(GlobalControllerAndView)
        self.pendingGroupBox.setMinimumSize(QtCore.QSize(0, 55))
        self.pendingGroupBox.setMaximumSize(QtCore.QSize(16777215, 55))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pendingGroupBox.setFont(font)
        self.pendingGroupBox.setObjectName(_fromUtf8("pendingGroupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.pendingGroupBox)
        self.horizontalLayout_2.setMargin(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pendingSendButton = QtGui.QPushButton(self.pendingGroupBox)
        self.pendingSendButton.setObjectName(_fromUtf8("pendingSendButton"))
        self.horizontalLayout.addWidget(self.pendingSendButton)
        self.pendingCancelButton = QtGui.QPushButton(self.pendingGroupBox)
        self.pendingCancelButton.setObjectName(_fromUtf8("pendingCancelButton"))
        self.horizontalLayout.addWidget(self.pendingCancelButton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_5.addWidget(self.pendingGroupBox)
        self.singleLineTextEdit = QtGui.QTextEdit(GlobalControllerAndView)
        self.singleLineTextEdit.setMaximumSize(QtCore.QSize(400, 16777215))
        self.singleLineTextEdit.setReadOnly(True)
        self.singleLineTextEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.singleLineTextEdit.setObjectName(_fromUtf8("singleLineTextEdit"))
        self.horizontalLayout_5.addWidget(self.singleLineTextEdit)
        self.messageTextEdit = QtGui.QTextEdit(GlobalControllerAndView)
        self.messageTextEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.messageTextEdit.setMaximumSize(QtCore.QSize(16777215, 57))
        self.messageTextEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.messageTextEdit.setObjectName(_fromUtf8("messageTextEdit"))
        self.horizontalLayout_5.addWidget(self.messageTextEdit)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)

        self.retranslateUi(GlobalControllerAndView)
        QtCore.QMetaObject.connectSlotsByName(GlobalControllerAndView)

    def retranslateUi(self, GlobalControllerAndView):
        GlobalControllerAndView.setWindowTitle(_translate("GlobalControllerAndView", "Form", None))
        self.pendingGroupBox.setTitle(_translate("GlobalControllerAndView", "pending Commands", None))
        self.pendingSendButton.setText(_translate("GlobalControllerAndView", "send", None))
        self.pendingCancelButton.setText(_translate("GlobalControllerAndView", "cancel", None))

