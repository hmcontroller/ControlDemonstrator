# -*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from core.command import Command
from gui.designerfiles.commandSettingsDialog import Ui_CommandSettingsDialog
from gui.resources import *

class CommandSettingsDialog(QtGui.QDialog, Ui_CommandSettingsDialog):
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
        self.tableWidget.setColumnHidden(8, True)

        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 60)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 80)
        self.tableWidget.setColumnWidth(5, 80)
        self.tableWidget.setColumnWidth(6, 80)
        self.tableWidget.setColumnWidth(7, 30)

        horItemOne = QtGui.QTableWidgetItem("Id")
        horItemOne.setTextAlignment(QtCore.Qt.AlignLeft)
        self.tableWidget.setHorizontalHeaderItem(2, horItemOne)

        self.tableWidget.setHorizontalHeaderLabels([u"Variablenname",
                                                    u"Anzeigename",
                                                    u"pending",
                                                    u"Eingabe per",
                                                    u"Min",
                                                    u"Max",
                                                    u"Startwert",
                                                    u"" ])

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
            if commandId > newId:
                newId = commandId + 1
        self.finalCommandIDs.append(newId)
        self.setCommandsToTable()

    def setCommandsToTable(self):
        self.tableWidget.clear()
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
            self.tableWidget.setItem(i, 0, nameItem)

            displayNameItem = QtGui.QTableWidgetItem(unicode(command.displayName))
            self.tableWidget.setItem(i, 1, displayNameItem)

            pendingItem = QtGui.QTableWidgetItem()
            pendingItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            if command._pendingSendMode is True:
                pendingItem.setCheckState(QtCore.Qt.Checked)
            else:
                pendingItem.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget.setItem(i, 2, pendingItem)

            inputMethodItem = QtGui.QTableWidgetItem()
            comboBox = QtGui.QComboBox()
            indexToSelect = 0
            for n, mode in enumerate(self.inputModes):
                comboBox.addItem(mode[1])
                if mode[0] == command.inputMethod:
                    indexToSelect = n
            comboBox.setCurrentIndex(indexToSelect)
            self.tableWidget.setCellWidget(i, 3, comboBox)

            lowerLimitItem = QtGui.QTableWidgetItem(unicode(command._lowerLimit))
            self.tableWidget.setItem(i, 4, lowerLimitItem)

            upperLimitItem = QtGui.QTableWidgetItem(unicode(command._upperLimit))
            self.tableWidget.setItem(i, 5, upperLimitItem)

            valueItem = QtGui.QTableWidgetItem(unicode(command._value))
            self.tableWidget.setItem(i, 6, valueItem)


            pixmap = QtGui.QPixmap(redCrossPngPath)
            qIcon = QtGui.QIcon(pixmap)
            iconItem = QtGui.QTableWidgetItem()
            iconItem.setIcon(qIcon)
            iconItem.setToolTip("delete")
            self.tableWidget.setItem(i, 7, iconItem)

            idItem = QtGui.QTableWidgetItem(str(commandId))
            self.tableWidget.setItem(i, 8, idItem)


    def updateSettings(self):


        # set settings to form


        answer = self.exec_()

        if answer == QtGui.QDialog.Accepted:
            for i in range(0, self.tableWidget.rowCount()):
                id = int(self.tableWidget.item(i, 8).text())
                self.commands[id].name = unicode(self.tableWidget.item(i, 0).text())
                self.commands[id].displayName = unicode(self.tableWidget.item(i, 1).text())
                if self.tableWidget.item(i, 2).checkState() == QtCore.Qt.Checked:
                    self.commands[id].setPendingSendMode(True)
                else:
                    self.commands[id].setPendingSendMode(False)
                comboIndex = self.tableWidget.cellWidget(i, 3).currentIndex()
                self.commands[id].inputMethod = self.inputModes[comboIndex][0]

                self.commands[id].setLowerLimit(float(self.tableWidget.item(i, 4).text()))
                self.commands[id].setUpperLimit(float(self.tableWidget.item(i, 5).text()))
                self.commands[id].setValue(float(self.tableWidget.item(i, 6).text()))

        else:
            print "dann nicht"


