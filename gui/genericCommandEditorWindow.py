# -*- encoding: utf-8 -*-

from PyQt4 import QtCore

from gui.constants import *
from gui.graphicItems.commandWidgets.genericCommand import GenericCommandWithoutMinMaxEdit


class GenericCommandEditorWindow(QtGui.QDialog):

    parameterChanged = QtCore.pyqtSignal(int, float)

    def __init__(self, commands, parent=None):
        super(GenericCommandEditorWindow, self).__init__(parent)

        self.setWindowTitle("Parametereditor")

        self.mainLayout = QtGui.QHBoxLayout(self)
        self.mainLayout.setMargin(0)

        self.graphicsView = QtGui.QGraphicsView()
        self.mainLayout.addWidget(self.graphicsView)

        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.graphicsView.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.commands = commands

        self.graphicsView.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.lightGray))
        self.graphicsView.setStyleSheet("""
            .ControllerGeneric {
                border-style: none;
                }
            """)

        self.scene = QtGui.QGraphicsScene()

        self.items = list()
        for command in self.commands:
            commandItem = GenericCommandWithoutMinMaxEdit(command)
            self.scene.addItem(commandItem)
            self.items.append(commandItem)

        self.graphicsView.setScene(self.scene)

        self.contentWidth = 0
        self.contentHeight = 0

        self.arrangeItems()

        # if i open a window here to let the user edit some properties, it needs to be updated to show
        #  warnings, if some are active.
        self.updateTimer = QtCore.QTimer()
        self.updateTimer.setSingleShot(False)
        self.updateTimer.timeout.connect(self.update)
        self.updateTimer.start(100)



    def update(self):
        # if self.contentHeight > self.graphicsView.height():
        #     self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # else:
        #     self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        for item in self.items:
            item.update()

        self.scene.setSceneRect(0, 0, self.contentWidth, self.contentHeight)
        self.scene.update()
        # self.resize(self.width(), self.height())

    def arrangeItems(self):
        row = 0
        for item in self.items:
            positionX = 0
            positionY = row * item.height
            item.setPos(positionX, positionY)
            row += 1

        if len(self.items) > 0:
            self.contentWidth = self.items[-1].width # + 20
            self.contentHeight = row * self.items[-1].height # + 20
        else:
            self.contentWidth = 0
            self.contentHeight = 0
        self.setGeometry(100, 100, self.contentWidth, self.contentHeight)

        self.setFixedSize(self.contentWidth, self.contentHeight)

        self.update()

    def updateSymbols(self):
        self.scene.update()

    def resizeEvent(self, QResizeEvent):
        super(GenericCommandEditorWindow, self).resizeEvent(QResizeEvent)
