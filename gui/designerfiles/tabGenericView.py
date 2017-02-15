# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tabGenericView.ui'
#
# Created: Wed Feb 15 13:00:37 2017
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

class Ui_tabGenericView(object):
    def setupUi(self, tabGenericView):
        tabGenericView.setObjectName(_fromUtf8("tabGenericView"))
        tabGenericView.resize(919, 635)
        self.horizontalLayout_3 = QtGui.QHBoxLayout(tabGenericView)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.splitter = QtGui.QSplitter(tabGenericView)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.commandViewLayout = QtGui.QHBoxLayout(self.widget)
        self.commandViewLayout.setMargin(0)
        self.commandViewLayout.setObjectName(_fromUtf8("commandViewLayout"))
        self.label_1 = QtGui.QLabel(self.widget)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.commandViewLayout.addWidget(self.label_1)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.commandViewLayout.addWidget(self.label_2)
        self.widget1 = QtGui.QWidget(self.splitter)
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.plotLayout = QtGui.QHBoxLayout(self.widget1)
        self.plotLayout.setMargin(0)
        self.plotLayout.setObjectName(_fromUtf8("plotLayout"))
        self.label_3 = QtGui.QLabel(self.widget1)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.plotLayout.addWidget(self.label_3)
        self.label_4 = QtGui.QLabel(self.widget1)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.plotLayout.addWidget(self.label_4)
        self.horizontalLayout_3.addWidget(self.splitter)

        self.retranslateUi(tabGenericView)
        QtCore.QMetaObject.connectSlotsByName(tabGenericView)

    def retranslateUi(self, tabGenericView):
        tabGenericView.setWindowTitle(_translate("tabGenericView", "Form", None))
        self.label_1.setText(_translate("tabGenericView", "command view", None))
        self.label_2.setText(_translate("tabGenericView", "command view", None))
        self.label_3.setText(_translate("tabGenericView", "command view", None))
        self.label_4.setText(_translate("tabGenericView", "command view", None))

