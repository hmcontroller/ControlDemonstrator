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
    DELETE_COLUMN = 7
    ID_COLUMN = 8

    def __init__(self, commands, parent=None):
        super(CommandSettingsDialog, self).__init__(parent)
        self.setupUi(self)

        self.commands = commands
        self.finalCommandIDs = list()

        for command in self.commands:
            self.finalCommandIDs.append(command.id)


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
        self.tableHeader.setResizeMode(self.DELETE_COLUMN, QtGui.QHeaderView.Fixed)

        self.tableWidget.setColumnHidden(self.ID_COLUMN, True)


        columnNames = [u"Variablenname",
                       u"Anzeigename",
                       u"Min",
                       u"Max",
                       u"Startwert",
                       u"pending",
                       u"Eingabe per",
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
        self.tableWidget.setColumnWidth(self.MIN_COLUMN, 80)
        self.tableWidget.setColumnWidth(self.MAX_COLUMN, 80)
        self.tableWidget.setColumnWidth(self.START_VALUE_COLUMN, 80)
        self.tableWidget.setColumnWidth(self.DELETE_COLUMN, 24)


        self.inputModes = list()
        self.inputModes.append((Command.VALUE_INPUT, "Wert"))
        self.inputModes.append((Command.SWITCH_INPUT, "Schalter"))
        self.inputModes.append((Command.TOGGLE_INPUT, "Taster"))

        self.setCommandsToTable()

        self.tableWidget.cellChanged.connect(self.cellChanged)
        self.tableWidget.cellClicked.connect(self.cellClicked)

        plusPixmap = QtGui.QPixmap(greenPlusPath)
        plusIcon = QtGui.QIcon(plusPixmap)
        self.toolButtonAddChannel.setIcon(plusIcon)
        self.toolButtonAddChannel.clicked.connect(self.addCommand)


    def cellChanged(self, row, column):
        pass

    def cellClicked(self, row, column):
        if column == 7:
            idToDelete = int(self.tableWidget.item(row, 8).text())
            self.removeCommand(idToDelete)


    def removeCommand(self, id):
        for i in range(0, len(self.finalCommandIDs)):
            if self.finalCommandIDs[i] == id:
                self.finalCommandIDs.pop(i)
                break
        self.setCommandsToTable()

    def addCommand(self):
        newId = 0
        for commandId in self.finalCommandIDs:
            if commandId >= newId:
                newId = commandId + 1
        self.finalCommandIDs.append(newId)
        self.setCommandsToTable()

    def setCommandsToTable(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(self.finalCommandIDs))

        for i, commandId in enumerate(self.finalCommandIDs):
            try:
                command = self.commands.getCommandById(commandId)
            except Exception:
                command = Command()
                command.id = commandId
                command.name = "new"
                command.displayName = u"Neu"

            nameItem = QtGui.QTableWidgetItem(unicode(command.name))
            self.tableWidget.setItem(i, self.VARIABLE_NAME_COLUMN, nameItem)

            displayNameItem = QtGui.QTableWidgetItem(unicode(command.displayName))
            self.tableWidget.setItem(i, self.DISPLAY_NAME_COLUMN, displayNameItem)

            pendingItem = QtGui.QTableWidgetItem()
            pendingItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            if command._pendingSendMode is True:
                pendingItem.setCheckState(QtCore.Qt.Checked)
            else:
                pendingItem.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget.setItem(i, self.PENDING_COLUMN, pendingItem)

            inputMethodItem = QtGui.QTableWidgetItem()
            comboBox = QtGui.QComboBox()
            indexToSelect = 0
            for n, mode in enumerate(self.inputModes):
                comboBox.addItem(mode[1])
                if mode[0] == command.inputMethod:
                    indexToSelect = n
            comboBox.setCurrentIndex(indexToSelect)
            self.tableWidget.setCellWidget(i, self.INPUT_METHOD_COLUMN, comboBox)

            lowerLimitItem = QtGui.QTableWidgetItem(unicode(command._lowerLimit))
            self.tableWidget.setItem(i, self.MIN_COLUMN, lowerLimitItem)

            upperLimitItem = QtGui.QTableWidgetItem(unicode(command._upperLimit))
            self.tableWidget.setItem(i, self.MAX_COLUMN, upperLimitItem)

            valueItem = QtGui.QTableWidgetItem(unicode(command._value))
            self.tableWidget.setItem(i, self.START_VALUE_COLUMN, valueItem)


            pixmap = QtGui.QPixmap(redCrossPngPath)
            qIcon = QtGui.QIcon(pixmap)
            iconItem = QtGui.QTableWidgetItem()
            iconItem.setIcon(qIcon)
            iconItem.setToolTip("delete")
            self.tableWidget.setItem(i, self.DELETE_COLUMN, iconItem)

            idItem = QtGui.QTableWidgetItem(str(commandId))
            self.tableWidget.setItem(i, self.ID_COLUMN, idItem)

    def resizeDialogToTableWidth(self, logicalIndex=0, oldSize=0, newSize=0):
        print "tableWidth", self.tableWidget.width()

        widthSum = 0
        for i in range(0, self.tableWidget.columnCount()):
            widthSum += self.tableWidget.columnWidth(i)

        self.resize(widthSum + 24, 700)



    def updateSettings(self):

        self.resizeDialogToTableWidth()

        # set settings to form

        answer = self.exec_()

        if answer == QtGui.QDialog.Accepted:
            for i in range(0, self.tableWidget.rowCount()):
                id = int(self.tableWidget.item(i, self.ID_COLUMN).text())
                self.commands[id].name = unicode(self.tableWidget.item(i, self.VARIABLE_NAME_COLUMN).text())
                self.commands[id].displayName = unicode(self.tableWidget.item(i, self.DISPLAY_NAME_COLUMN).text())
                if self.tableWidget.item(i, self.PENDING_COLUMN).checkState() == QtCore.Qt.Checked:
                    self.commands[id].setPendingSendMode(True)
                else:
                    self.commands[id].setPendingSendMode(False)
                comboIndex = self.tableWidget.cellWidget(i, self.INPUT_METHOD_COLUMN).currentIndex()
                self.commands[id].inputMethod = self.inputModes[comboIndex][0]

                self.commands[id].setLowerLimit(float(self.tableWidget.item(i, self.MIN_COLUMN).text()))
                self.commands[id].setUpperLimit(float(self.tableWidget.item(i, self.MAX_COLUMN).text()))
                self.commands[id].setValue(float(self.tableWidget.item(i, self.START_VALUE_COLUMN).text()))

        else:
            print "dann nicht"


