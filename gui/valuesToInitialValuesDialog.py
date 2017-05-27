# -*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from core.valueChannel import ValueChannel

from gui.designerfiles.valuesToInitialValuesDialog import Ui_valuesToInitialValuesDialog
from gui.resources import *

class ValuesToInitialValuesDialog(QtGui.QDialog, Ui_valuesToInitialValuesDialog):

    SELECT_COLUMN = 0
    VARIABLE_NAME_COLUMN = 1
    DISPLAY_NAME_COLUMN = 2
    HIDDEN_ID_COLUMN = 3

    def __init__(self, commands, parent=None):
        super(ValuesToInitialValuesDialog, self).__init__(parent)
        self.setupUi(self)

        self.commands = commands

        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setFrameStyle(QtGui.QFrame.NoFrame)
        self.tableWidget.setColumnCount(4)

        self.tableHeader = QtGui.QHeaderView(QtCore.Qt.Horizontal, self.tableWidget)
        self.tableWidget.setHorizontalHeader(self.tableHeader)

        self.tableHeader.setResizeMode(QtGui.QHeaderView.Stretch)

        self.tableHeader.setResizeMode(self.SELECT_COLUMN, QtGui.QHeaderView.Fixed)
        self.tableHeader.setResizeMode(self.VARIABLE_NAME_COLUMN, QtGui.QHeaderView.Interactive)
        self.tableHeader.setResizeMode(self.DISPLAY_NAME_COLUMN, QtGui.QHeaderView.Stretch)

        self.tableWidget.setColumnHidden(self.HIDDEN_ID_COLUMN, True)

        columnNames = [u"" ,u"Variablenname", u"Anzeigename"]

        for i, name in enumerate(columnNames):
            horItem = QtGui.QTableWidgetItem(name)
            horItem.setTextAlignment(QtCore.Qt.AlignLeft)
            horItem.setBackground(QtGui.QBrush(QtCore.Qt.darkGray))
            self.tableWidget.setHorizontalHeaderItem(i, horItem)

        self.tableWidget.horizontalHeader().setStyleSheet(" QHeaderView::section { "
                        "spacing: 10px; background-color: lightgray; border: 3px solid lightgray; }")

        self.tableWidget.setColumnWidth(self.SELECT_COLUMN, 32)
        self.tableWidget.setColumnWidth(self.VARIABLE_NAME_COLUMN, 250)
        self.tableWidget.setColumnWidth(self.DISPLAY_NAME_COLUMN, 250)

        self.initializeTable()

        self.pushButtonSelectAll.clicked.connect(self.selectAll)
        self.pushButtonDeselectAll.clicked.connect(self.deselectAll)

    def doIt(self):

        self.resizeDialogToTableWidth()

        answer = self.exec_()

        if answer == QtGui.QDialog.Accepted:

            for rowNumber, command in enumerate(self.commands):
                if self.tableWidget.item(rowNumber, self.SELECT_COLUMN).checkState() == QtCore.Qt.Checked:
                    command.initialValue = command._value

            return self.commands

        else:
            return self.commands



    def initializeTable(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        for command in self.commands:
            self.addChannelToTable(command)

    def addChannelToTable(self, command):

        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)

        selectItem = QtGui.QTableWidgetItem()
        selectItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        selectItem.setCheckState(QtCore.Qt.Checked)
        self.tableWidget.setItem(row, self.SELECT_COLUMN, selectItem)

        nameItem = QtGui.QTableWidgetItem(unicode(command.name))
        self.tableWidget.setItem(row, self.VARIABLE_NAME_COLUMN, nameItem)

        displayNameItem = QtGui.QTableWidgetItem(unicode(command.displayName))
        self.tableWidget.setItem(row, self.DISPLAY_NAME_COLUMN, displayNameItem)

        idItem = QtGui.QTableWidgetItem(unicode(command.id))
        self.tableWidget.setItem(row, self.HIDDEN_ID_COLUMN, idItem)

    def selectAll(self):
        for rowNumber in range(0, self.tableWidget.rowCount()):
            self.tableWidget.item(rowNumber, self.SELECT_COLUMN).setCheckState(QtCore.Qt.Checked)

    def deselectAll(self):
        for rowNumber in range(0, self.tableWidget.rowCount()):
            self.tableWidget.item(rowNumber, self.SELECT_COLUMN).setCheckState(QtCore.Qt.Unchecked)

    def resizeDialogToTableWidth(self, logicalIndex=0, oldSize=0, newSize=0):
        widthSum = 0
        for i in range(0, self.tableWidget.columnCount()):
            widthSum += self.tableWidget.columnWidth(i)

        self.resize(widthSum + 24, 700)

