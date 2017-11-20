# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'globalControllerAndView.ui'
#
# Created: Mon Nov 20 13:36:23 2017
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
        GlobalControllerAndView.resize(1645, 73)
        GlobalControllerAndView.setMaximumSize(QtCore.QSize(16777215, 73))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(GlobalControllerAndView)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.pendingGroupBox_2 = QtGui.QGroupBox(GlobalControllerAndView)
        self.pendingGroupBox_2.setMinimumSize(QtCore.QSize(0, 55))
        self.pendingGroupBox_2.setMaximumSize(QtCore.QSize(16777215, 120))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pendingGroupBox_2.setFont(font)
        self.pendingGroupBox_2.setObjectName(_fromUtf8("pendingGroupBox_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.pendingGroupBox_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pendingSendButton = QtGui.QPushButton(self.pendingGroupBox_2)
        self.pendingSendButton.setMinimumSize(QtCore.QSize(0, 25))
        self.pendingSendButton.setObjectName(_fromUtf8("pendingSendButton"))
        self.horizontalLayout_3.addWidget(self.pendingSendButton)
        self.pendingCancelButton = QtGui.QPushButton(self.pendingGroupBox_2)
        self.pendingCancelButton.setMinimumSize(QtCore.QSize(0, 25))
        self.pendingCancelButton.setObjectName(_fromUtf8("pendingCancelButton"))
        self.horizontalLayout_3.addWidget(self.pendingCancelButton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.pendingGroupBox_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.toolButton = QtGui.QToolButton(GlobalControllerAndView)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton.sizePolicy().hasHeightForWidth())
        self.toolButton.setSizePolicy(sizePolicy)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.verticalLayout.addWidget(self.toolButton)
        self.pushButtonSerialMonitor = QtGui.QPushButton(GlobalControllerAndView)
        self.pushButtonSerialMonitor.setObjectName(_fromUtf8("pushButtonSerialMonitor"))
        self.verticalLayout.addWidget(self.pushButtonSerialMonitor)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.singleLineTextEdit = QtGui.QTextEdit(GlobalControllerAndView)
        self.singleLineTextEdit.setMaximumSize(QtCore.QSize(400, 16777215))
        self.singleLineTextEdit.setReadOnly(True)
        self.singleLineTextEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.singleLineTextEdit.setObjectName(_fromUtf8("singleLineTextEdit"))
        self.horizontalLayout.addWidget(self.singleLineTextEdit)
        self.messageTextEdit = QtGui.QTextEdit(GlobalControllerAndView)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.messageTextEdit.sizePolicy().hasHeightForWidth())
        self.messageTextEdit.setSizePolicy(sizePolicy)
        self.messageTextEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.messageTextEdit.setMaximumSize(QtCore.QSize(16777215, 130))
        self.messageTextEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.messageTextEdit.setObjectName(_fromUtf8("messageTextEdit"))
        self.horizontalLayout.addWidget(self.messageTextEdit)
        self.horizontalLayout_4.addLayout(self.horizontalLayout)

        self.retranslateUi(GlobalControllerAndView)
        QtCore.QMetaObject.connectSlotsByName(GlobalControllerAndView)

    def retranslateUi(self, GlobalControllerAndView):
        GlobalControllerAndView.setWindowTitle(_translate("GlobalControllerAndView", "Form", None))
        self.pendingGroupBox_2.setTitle(_translate("GlobalControllerAndView", "pending Commands", None))
        self.pendingSendButton.setText(_translate("GlobalControllerAndView", "send", None))
        self.pendingCancelButton.setText(_translate("GlobalControllerAndView", "cancel", None))
        self.toolButton.setText(_translate("GlobalControllerAndView", "...", None))
        self.pushButtonSerialMonitor.setText(_translate("GlobalControllerAndView", "SM", None))

