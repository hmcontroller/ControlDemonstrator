# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tabWaterLineExperiment.ui'
#
# Created: Tue Feb 21 12:14:50 2017
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

class Ui_tabWaterLineExperiment(object):
    def setupUi(self, tabWaterLineExperiment):
        tabWaterLineExperiment.setObjectName(_fromUtf8("tabWaterLineExperiment"))
        tabWaterLineExperiment.resize(919, 635)
        self.horizontalLayout = QtGui.QHBoxLayout(tabWaterLineExperiment)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayoutCommandView = QtGui.QVBoxLayout()
        self.verticalLayoutCommandView.setMargin(0)
        self.verticalLayoutCommandView.setObjectName(_fromUtf8("verticalLayoutCommandView"))
        self.label_1 = QtGui.QLabel(tabWaterLineExperiment)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.verticalLayoutCommandView.addWidget(self.label_1)
        self.horizontalLayoutPlotArea = QtGui.QHBoxLayout()
        self.horizontalLayoutPlotArea.setObjectName(_fromUtf8("horizontalLayoutPlotArea"))
        self.label_2 = QtGui.QLabel(tabWaterLineExperiment)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayoutPlotArea.addWidget(self.label_2)
        self.verticalLayoutCommandView.addLayout(self.horizontalLayoutPlotArea)
        self.horizontalLayout.addLayout(self.verticalLayoutCommandView)

        self.retranslateUi(tabWaterLineExperiment)
        QtCore.QMetaObject.connectSlotsByName(tabWaterLineExperiment)

    def retranslateUi(self, tabWaterLineExperiment):
        tabWaterLineExperiment.setWindowTitle(_translate("tabWaterLineExperiment", "Form", None))
        self.label_1.setText(_translate("tabWaterLineExperiment", "generic Command View", None))
        self.label_2.setText(_translate("tabWaterLineExperiment", "plot window", None))

