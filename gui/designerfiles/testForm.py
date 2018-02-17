# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testForm.ui'
#
# Created: Sat Feb 17 17:48:09 2018
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

class Ui_testForm(object):
    def setupUi(self, testForm):
        testForm.setObjectName(_fromUtf8("testForm"))
        testForm.resize(692, 579)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(testForm)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.toolButton = QtGui.QToolButton(testForm)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.horizontalLayout.addWidget(self.toolButton)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(testForm)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(testForm)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtGui.QLabel(testForm)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtGui.QLabel(testForm)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.listWidget = QtGui.QListWidget(testForm)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.retranslateUi(testForm)
        QtCore.QMetaObject.connectSlotsByName(testForm)

    def retranslateUi(self, testForm):
        testForm.setWindowTitle(_translate("testForm", "Form", None))
        self.toolButton.setText(_translate("testForm", "...", None))
        self.label.setText(_translate("testForm", "TextLabel", None))
        self.label_2.setText(_translate("testForm", "TextLabel", None))
        self.label_3.setText(_translate("testForm", "TextLabel", None))
        self.label_4.setText(_translate("testForm", "TextLabel", None))

