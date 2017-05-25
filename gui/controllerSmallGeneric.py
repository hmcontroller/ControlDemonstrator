# -*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from gui.graphicItems.commandWidgets.smallGenericCommand import SmallGenericCommand


class ControllerSmallGeneric(QtGui.QGraphicsView):

    parameterChanged = QtCore.pyqtSignal(int, float)

    def __init__(self, commands, channels, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)


        self.verticalScrollMode = True

        # the scroll bars will be manually shown or not from self.arrangeItems
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.commands = commands
        self.commands.changed.connect(self.commandListChanged)
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

        self.initItems()

        self.setScene(self.scene)

        self.arrangeItems()

    def initItems(self):
        self.scene.clear()
        self.items = list()
        for command in self.commands:
            commandItem = SmallGenericCommand(command)
            self.scene.addItem(commandItem)
            self.items.append(commandItem)

    def commandListChanged(self):
        self.initItems()
        self.arrangeItems()

    def arrangeItems(self):
        """
        All commands will be arranged in a grid, that either fits horizontally or vertically
        depending on the value of self.verticalScrollMode.

        If verticalScrollMode is True, a horizontal scrollbar will appear and
        only so many rows are drawn, that they fit in the available vertical space.

        If verticalScrollMode is False, a vertical scrollbar will appear and
        only so many columns are drawn, that they fit in the available horizontal space.
        """

        # adjust here for the size of possible scrollbars
        maxHeight = self.height() - 20
        maxWidth = self.width() - 20


        # position the commandItems in a grid
        column = 0
        row = 0
        if self.verticalScrollMode is True:
            # arrange for a vertical scroll bar
            for item in self.items:
                rightCornerPosition = column * item.width + item.width
                if rightCornerPosition > maxWidth:
                    column = 0
                    row += 1
                positionX = column * item.width
                positionY = row * item.height # + 100
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

        # calculate the new width and height
        if len(self.items) > 0:
            totalWidth = column * self.items[-1].width + self.items[-1].width + 20
            totalHeight = row * self.items[-1].height + self.items[-1].height + 20
        else:
            totalWidth = 0
            totalHeight = 0

        # show scrollbars if needed
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
        super(ControllerSmallGeneric, self).resizeEvent(QResizeEvent)
        self.arrangeItems()
