# -*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore


from gui.singleChannelSettingsConfig import SingleChannelSettingsConfig

class IdColorLabelCheckbox(QtGui.QWidget):

    changed = QtCore.pyqtSignal(int, int)
    keyPressed = QtCore.pyqtSignal(object)

    def __init__(self, parent=None, channel=None, id=None, color=None):
        super(IdColorLabelCheckbox, self).__init__(parent)
        self.id = id
        self.color = color

        self.channel = channel
        self.channel.changed.connect(self.channelChanged)
        self.channel.showChanged.connect(self.channelChanged)
        self.channel.requestedChanged.connect(self.channelChanged)
        self.channel.colorChanged.connect(self.channelChanged)
        self.channel.scaleFactorChanged.connect(self.channelChanged)


        verticalLayout = QtGui.QVBoxLayout(self)

        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setMargin(0)
        horizontalLayout.setSpacing(6)

        verticalLayout.addLayout(horizontalLayout)
        verticalLayout.setMargin(0)
        verticalLayout.setSpacing(6)
        verticalLayout.setContentsMargins(0, 3, 0, 3)

        self.checkBox = CheckBoxWithoutKeyPress()
        self.checkBox.keyPressed.connect(self.keyPressed)
        self.colorBox = ColouredRectangle(self.color)
        self.colorBox.clicked.connect(self.mousePressEvent)
        self.label = ClickableLabel()
        self.label.clicked.connect(self.mousePressEvent)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.label.setSizePolicy(sizePolicy)

        self.setSizePolicy(sizePolicy)



        horizontalLayout.setAlignment(QtCore.Qt.AlignLeft)
        horizontalLayout.addWidget(self.checkBox)
        horizontalLayout.addWidget(self.colorBox)
        horizontalLayout.addWidget(self.label)

        self.lowerHorizontalLayout = QtGui.QHBoxLayout()
        verticalLayout.addLayout(self.lowerHorizontalLayout)

        self.scaleLabel = QtGui.QLabel("Scale 1.2")
        self.lowerHorizontalLayout.addWidget(self.scaleLabel)
        self.scaleLabel.setStyleSheet("QLabel { color : red; }")

        self.valueLabel = QtGui.QLabel("---")
        self.valueLabel.setSizePolicy(sizePolicy)

        self.lowerHorizontalLayout.addWidget(self.valueLabel)
        self.lowerHorizontalLayout.setAlignment(QtCore.Qt.AlignTop)


        # spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        # verticalLayout.addItem(spacerItem)

        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtCore.Qt.darkGray)
        # self.setAutoFillBackground(True)
        # self.setPalette(pal)


        minHeight = 0
        minHeight += self.colorBox.size().height()
        minHeight += self.valueLabel.size().height()
        # minHeight += 40

        minWidth = 0
        minWidth += self.checkBox.size().width()
        minWidth += self.colorBox.size().width()
        minWidth += self.label.size().width()
        # self.setMinimumSize(minWidth, minHeight)

        self.overlay = OverlayDrawing(self)
        self.overlay.setGeometry(0, 0, 300, 50)
        self.overlay.hide()


        self.checkBox.stateChanged.connect(self.statiChanged)

    def setValue(self, value):
        self.valueLabel.setText(value)

    @QtCore.pyqtSlot(object)
    def setScale(self, valueChannel):
        self.scaleLabel.setText("Scale {}".format(valueChannel.displayScaleFactor))
        if valueChannel.displayScaleFactor == 1.0:
            self.scaleLabel.hide()
        else:
            self.scaleLabel.show()

    def changeState(self):
        if self.channel.isRequested is False:
            return
        currentState = self.checkBox.checkState()
        if currentState == QtCore.Qt.Checked:
           self.checkBox.setCheckState(QtCore.Qt.Unchecked)
        else:
            self.checkBox.setCheckState(QtCore.Qt.Checked)

    def statiChanged(self, state):
        self.changed.emit(self.id, state)

    def setText(self, text):
        self.label.setText(text)

    def setChecked(self, value):
        self.checkBox.setChecked(value)

    def setRequested(self, value):
        if value is True:
            self.overlay.hide()
        else:
            self.overlay.show()


    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == QtCore.Qt.LeftButton:
            self.changeState()

        if QMouseEvent.button() == QtCore.Qt.RightButton:
            self.changeChannelConfig()

    def size(self):
        return QtCore.QSize(200, 50)

    # def changeChannelColor(self):
    #     colorDialog = QtGui.QColorDialog()
    #     answer = colorDialog.exec_()
    #     if answer == QtGui.QDialog.Accepted:
    #         color = colorDialog.selectedColor()
    #         colorTuple = (color.red(), color.green(), color.blue())
    #         self.channel.colorRgbTuple = colorTuple
    #         self.colorBox.brush = QtGui.QBrush(color)

    def changeChannelDisplayScale(self):
        pass

    @QtCore.pyqtSlot(object)
    def channelChanged(self, channel):
        if len(channel.displayName) > 0:
            self.setText(channel.displayName)
        else:
            self.setText(channel.name)

        self.setScale(channel)
        self.colorBox.brush = QtGui.QBrush(QtGui.QColor(channel.colorRgbTuple[0], channel.colorRgbTuple[1], channel.colorRgbTuple[2]))

    def changeChannelConfig(self):
        SingleChannelSettingsConfig.updateSettings(self.channel)


class ColouredRectangle(QtGui.QWidget):

    clicked = QtCore.pyqtSignal(object)

    def __init__(self, color, parent=None):
        super(ColouredRectangle, self).__init__(parent)
        self.widthInPixels = 15
        self.heightInPixels = 15
        self.setGeometry(0, 0, self.widthInPixels, self.heightInPixels)
        self.setMinimumWidth(self.widthInPixels)
        self.brush = QtGui.QBrush(color)
        self.brush.setStyle(QtCore.Qt.SolidPattern)

        self.path = QtGui.QPainterPath()
        self.path.moveTo(0, 0)
        self.path.lineTo(self.widthInPixels, 0)
        self.path.lineTo(self.widthInPixels, self.heightInPixels)
        self.path.lineTo(0, self.heightInPixels)
        self.path.closeSubpath()

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.fillPath(self.path, self.brush)


    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.widthInPixels, self.heightInPixels)

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit(QMouseEvent)


class CheckBoxWithoutKeyPress(QtGui.QCheckBox):

    keyPressed = QtCore.pyqtSignal(object)

    def __init__(self):
        super(CheckBoxWithoutKeyPress, self).__init__()

    def keyPressEvent(self, qKeyEvent):
        self.keyPressed.emit(qKeyEvent)



class ClickableLabel(QtGui.QLabel):

    clicked = QtCore.pyqtSignal(object)

    def __init__(self):
        super(ClickableLabel, self).__init__()

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit(QMouseEvent)



class OverlayDrawing(QtGui.QWidget):
    def __init__(self, parent=None):
        super(OverlayDrawing, self).__init__(parent)
        self.parent = parent
        self.color = QtGui.QColor(200, 200, 200, 150)
        # self.color = QtGui.QColor(QtCore.Qt.red)
        self.brush = QtGui.QBrush(self.color)
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.height = 50

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)

    def paintEvent(self, qPaintEvent):
        super(OverlayDrawing, self).paintEvent(qPaintEvent)
        painter = QtGui.QPainter()
        painter.begin(self)
        width = self.geometry().width()
        painter.fillRect(0, 0, width, self.height, self.brush)

