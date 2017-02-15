# -*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from gui.graphicItems.commandWidgets.genericCommand import GenericCommand


class ControllerGeneric(QtGui.QGraphicsView):

    parameterChanged = QtCore.pyqtSignal(int, float)

    def __init__(self, commands, channels, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)


        self.verticalScrollMode = False

        # self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # if self.verticalScrollMode is True:
        #     self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #     self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        # else:
        #     self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        #     self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.commands = commands
        self.channels = channels

        self.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.lightGray))
        self.setStyleSheet("""
            .ControllerGeneric {
                border-style: none;
                }
            """)

        self.scene = QtGui.QGraphicsScene()

        self.cablePen = QtGui.QPen()
        self.cablePen.setColor(QtGui.QColor(0, 0, 0))
        self.cablePen.setWidth(2)
        self.cablePen.setCosmetic(True)

        self.items = list()
        for command in self.commands:
            commandItem = GenericCommand(command)
            self.scene.addItem(commandItem)
            self.items.append(commandItem)

        self.setScene(self.scene)

        self.arrangeItems()


    def arrangeItems(self):
        column = 0
        row = 0
        maxHeight = self.height() - 20
        maxWidth = self.width() - 20

        # print maxHeight

        if self.verticalScrollMode is True:
            # arrange for a vertical scroll bar
            for item in self.items:
                rightCornerPosition = column * item.width + item.width
                if rightCornerPosition > maxWidth:
                    column = 0
                    row += 1
                positionX = column * item.width
                positionY = row * item.height
                item.setPos(positionX, positionY)
                column += 1
        else:
            # arrange for a horizontal scroll bar
            for item in self.items:
                lowerCornerPosition = row * item.height + item.height
                if lowerCornerPosition > maxHeight:
                    row = 0
                    column += 1
                positionX = column * item.width
                positionY = row * item.height
                item.setPos(positionX, positionY)
                row += 1

        if len(self.items) > 0:
            totalWidth = column * self.items[-1].width + self.items[-1].width + 20
            totalHeight = row * self.items[-1].height + self.items[-1].height + 20
        else:
            totalWidth = 0
            totalHeight = 0

        if self.verticalScrollMode is True:
            if totalHeight > self.height():
                self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            else:
                self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        else:
            if totalWidth > self.width():
                self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            else:
                self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.scene.setSceneRect(0, 0, totalWidth, totalHeight)
        self.scene.update()
        self.resize(self.width(), self.height())

    def updateSymbols(self):
        self.scene.update()

    def resizeEvent(self, QResizeEvent):
        self.emit(QtCore.SIGNAL("resize()"))
        self.arrangeItems()