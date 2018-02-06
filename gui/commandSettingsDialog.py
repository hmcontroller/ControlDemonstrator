# -*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from core.command import Command

from gui.designerfiles.commandSettingsDialog import Ui_CommandSettingsDialog
from gui.resources import *



class CommandSettingsDialog(QtGui.QDialog, Ui_CommandSettingsDialog):

    VARIABLE_NAME_COLUMN = 0
    DISPLAY_NAME_COLUMN = 1
    MIN_COLUMN = 2
    MAX_COLUMN = 3
    START_VALUE_COLUMN = 4
    PENDING_COLUMN = 5
    INPUT_METHOD_COLUMN = 6
    DATA_TYPE_COLUMN = 7
    DELETE_COLUMN = 8
    ID_COLUMN = 9

    def __init__(self, commands, parent=None):
        super(CommandSettingsDialog, self).__init__(parent)
        self.setupUi(self)

        self.commands = commands

        self.tableWidget.clear()

        self.tableWidget.setColumnCount(9)
        self.tableWidget.setRowCount(len(self.commands))
        self.tableWidget.verticalHeader().setVisible(False)

        self.tableHeader = QtGui.QHeaderView(QtCore.Qt.Horizontal, self.tableWidget)
        self.tableWidget.setHorizontalHeader(self.tableHeader)
        self.tableHeader.setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableHeader.setResizeMode(self.VARIABLE_NAME_COLUMN, QtGui.QHeaderView.Stretch)
        self.tableHeader.setResizeMode(self.DISPLAY_NAME_COLUMN, QtGui.QHeaderView.Interactive)
        self.tableHeader.setResizeMode(self.MIN_COLUMN, QtGui.QHeaderView.Interactive)
        self.tableHeader.setResizeMode(self.MAX_COLUMN, QtGui.QHeaderView.Interactive)
        self.tableHeader.setResizeMode(self.START_VALUE_COLUMN, QtGui.QHeaderView.Interactive)
        self.tableHeader.setResizeMode(self.PENDING_COLUMN, QtGui.QHeaderView.Fixed)
        self.tableHeader.setResizeMode(self.INPUT_METHOD_COLUMN, QtGui.QHeaderView.Fixed)
        self.tableHeader.setResizeMode(self.DATA_TYPE_COLUMN, QtGui.QHeaderView.Fixed)
        self.tableHeader.setResizeMode(self.DELETE_COLUMN, QtGui.QHeaderView.Fixed)

        self.tableWidget.setColumnHidden(self.ID_COLUMN, True)

        columnNames = [u"Variablenname",
                       u"Anzeigename",
                       u"Min",
                       u"Max",
                       u"Startwert",
                       u"pending",
                       u"Eingabe per",
                       u"Datentyp",
                       u"" ]

        for i, name in enumerate(columnNames):
            horItem = QtGui.QTableWidgetItem(name)
            horItem.setTextAlignment(QtCore.Qt.AlignLeft)
            horItem.setBackground(QtGui.QBrush(QtCore.Qt.darkGray))
            self.tableWidget.setHorizontalHeaderItem(i, horItem)

        self.tableWidget.horizontalHeader().setStyleSheet(" QHeaderView::section { "
                        "spacing: 10px; background-color: lightgray; border: 3px solid lightgray; }")


        self.tableWidget.setColumnWidth(self.VARIABLE_NAME_COLUMN, 200)
        self.tableWidget.setColumnWidth(self.DISPLAY_NAME_COLUMN, 200)
        self.tableWidget.setColumnWidth(self.PENDING_COLUMN, 60)
        self.tableWidget.setColumnWidth(self.INPUT_METHOD_COLUMN, 100)
        self.tableWidget.setColumnWidth(self.DATA_TYPE_COLUMN, 100)
        self.tableWidget.setColumnWidth(self.MIN_COLUMN, 80)
        self.tableWidget.setColumnWidth(self.MAX_COLUMN, 80)
        self.tableWidget.setColumnWidth(self.START_VALUE_COLUMN, 80)
        self.tableWidget.setColumnWidth(self.DELETE_COLUMN, 24)


        self.inputModes = list()
        self.inputModes.append((Command.VALUE_INPUT, "Wert"))
        self.inputModes.append((Command.SWITCH_INPUT, "Schalter"))
        self.inputModes.append((Command.TOGGLE_INPUT, "Taster"))

        self.initializeTable()

        self.tableWidget.cellClicked.connect(self.cellClicked)

        plusPixmap = QtGui.QPixmap(greenPlusPath)
        plusIcon = QtGui.QIcon(plusPixmap)
        self.toolButtonAddChannel.setIcon(plusIcon)
        self.toolButtonAddChannel.clicked.connect(self.createCommand)


    def updateSettings(self):

        self.resizeDialogToTableWidth()

        # set settings to form

        answer = self.exec_()

        if answer == QtGui.QDialog.Accepted:

            # remove all old commands
            self.commands.cmdList = list()

            for rowNumber in range(0, self.tableWidget.rowCount()):

                command = Command()

                command.id = rowNumber

                command.name = unicode(self.tableWidget.item(rowNumber, self.VARIABLE_NAME_COLUMN).text()).replace(" ", "")

                command.displayName = unicode(self.tableWidget.item(rowNumber, self.DISPLAY_NAME_COLUMN).text())

                if self.tableWidget.item(rowNumber, self.PENDING_COLUMN).checkState() == QtCore.Qt.Checked:
                    command.setPendingSendMode(True)
                else:
                    command.setPendingSendMode(False)

                comboIndexInputMethod = self.tableWidget.cellWidget(rowNumber, self.INPUT_METHOD_COLUMN).currentIndex()
                command.setInputMethod(self.inputModes[comboIndexInputMethod][0])

                comboIndexDataType = self.tableWidget.cellWidget(rowNumber, self.DATA_TYPE_COLUMN).currentIndex()
                command.setValueType(command.AVAILABLE_DATATYPES[comboIndexDataType]["type"])

                lowerLimit = self.tableWidget.item(rowNumber, self.MIN_COLUMN).text().replace(",", ".")
                upperLimit  = self.tableWidget.item(rowNumber, self.MAX_COLUMN).text().replace(",", ".")
                initialValue  = self.tableWidget.item(rowNumber, self.START_VALUE_COLUMN).text().replace(",", ".")

                try:
                    lowerLimit = float(lowerLimit)
                    upperLimit = float(upperLimit)
                    initialValue = float(initialValue)
                except:
                    box = QtGui.QMessageBox()
                    box.setText(u"wrong number format at line {}".format(rowNumber + 1))
                    box.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
                    box.exec_()
                    raise Exception("wrong number format")
                else:
                    command.setLowerLimit(lowerLimit)
                    command.setUpperLimit(upperLimit)
                    command.initialValue = (initialValue)

                self.commands.append(command)

            self.commands.changed.emit(self.commands)
            return self.commands

        else:
            return self.commands



    def cellClicked(self, row, column):
        if column == self.DELETE_COLUMN:
            self.removeCommandFromTable(row)


    def removeCommandFromTable(self, row):
        self.tableWidget.removeRow(row)

    def createCommand(self):
        # make a temp command to get the initial values of all properties
        tempCommand = Command()
        self.addCommandToTable(tempCommand)

    def addCommandToTable(self, command):
        rowNumber = self.tableWidget.rowCount()

        self.tableWidget.insertRow(rowNumber)

        nameItem = QtGui.QTableWidgetItem(unicode(command.name))
        self.tableWidget.setItem(rowNumber, self.VARIABLE_NAME_COLUMN, nameItem)

        displayNameItem = QtGui.QTableWidgetItem(unicode(command.displayName))
        self.tableWidget.setItem(rowNumber, self.DISPLAY_NAME_COLUMN, displayNameItem)

        pendingItem = QtGui.QTableWidgetItem()
        pendingItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        if command._pendingSendMode is True:
            pendingItem.setCheckState(QtCore.Qt.Checked)
        else:
            pendingItem.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget.setItem(rowNumber, self.PENDING_COLUMN, pendingItem)

        inputMethodItem = QtGui.QTableWidgetItem()
        comboBox = QtGui.QComboBox()
        indexToSelect = 0
        for n, mode in enumerate(self.inputModes):
            comboBox.addItem(mode[1])
            if mode[0] == command.getInputMethod():
                indexToSelect = n
        comboBox.setCurrentIndex(indexToSelect)
        self.tableWidget.setCellWidget(rowNumber, self.INPUT_METHOD_COLUMN, comboBox)

        dataTypeItem = QtGui.QTableWidgetItem()
        comboBoxDataType = QtGui.QComboBox()
        indexToSelect = 0
        for n, aDict in enumerate(command.AVAILABLE_DATATYPES):
            comboBoxDataType.addItem(aDict["displayName"])
            if command.getValueType() == aDict["type"]:
                indexToSelect = n
        comboBoxDataType.setCurrentIndex(indexToSelect)
        self.tableWidget.setCellWidget(rowNumber, self.DATA_TYPE_COLUMN, comboBoxDataType)

        lowerLimitItem = QtGui.QTableWidgetItem(unicode(command._lowerLimit))
        self.tableWidget.setItem(rowNumber, self.MIN_COLUMN, lowerLimitItem)

        upperLimitItem = QtGui.QTableWidgetItem(unicode(command._upperLimit))
        self.tableWidget.setItem(rowNumber, self.MAX_COLUMN, upperLimitItem)

        initialValueItem = QtGui.QTableWidgetItem(unicode(command.initialValue))
        self.tableWidget.setItem(rowNumber, self.START_VALUE_COLUMN, initialValueItem)


        pixmap = QtGui.QPixmap(redCrossPngPath)
        qIcon = QtGui.QIcon(pixmap)
        iconItem = QtGui.QTableWidgetItem()
        iconItem.setIcon(qIcon)
        iconItem.setToolTip("delete")
        self.tableWidget.setItem(rowNumber, self.DELETE_COLUMN, iconItem)

        idItem = QtGui.QTableWidgetItem(str(command.id))
        self.tableWidget.setItem(rowNumber, self.ID_COLUMN, idItem)


    def initializeTable(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        for command in self.commands:
            self.addCommandToTable(command)

    def resizeDialogToTableWidth(self, logicalIndex=0, oldSize=0, newSize=0):
        widthSum = 0
        for i in range(0, self.tableWidget.columnCount()):
            widthSum += self.tableWidget.columnWidth(i)

        self.resize(widthSum + 24, 700)



