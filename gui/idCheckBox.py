# -*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore


class IdColorLabelCheckbox(QtGui.QWidget):

    changed = QtCore.pyqtSignal(int, int)
    keyPressed = QtCore.pyqtSignal(object)

    def __init__(self, parent=None, id=None, color=None):
        super(IdColorLabelCheckbox, self).__init__(parent)
        self.id = id
        self.color = color

        verticalLayout = QtGui.QVBoxLayout(self)

        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setMargin(0)
        horizontalLayout.setSpacing(6)

        verticalLayout.addLayout(horizontalLayout)
        verticalLayout.setMargin(0)
        verticalLayout.setSpacing(6)

        self.checkBox = CheckBoxWithoutKeyPress()
        self.checkBox.keyPressed.connect(self.keyPressed)
        self.colorBox = ColouredRectangle(self.color)
        self.colorBox.clicked.connect(self.changeState)
        self.label = ClickableLabel()
        self.label.clicked.connect(self.changeState)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.label.setSizePolicy(sizePolicy)

        self.setSizePolicy(sizePolicy)



        horizontalLayout.setAlignment(QtCore.Qt.AlignLeft)
        horizontalLayout.addWidget(self.checkBox)
        horizontalLayout.addWidget(self.colorBox)
        horizontalLayout.addWidget(self.label)

        self.valueLabel = QtGui.QLabel("---")
        self.valueLabel.setSizePolicy(sizePolicy)


        verticalLayout.addWidget(self.valueLabel)
        verticalLayout.setAlignment(QtCore.Qt.AlignTop)


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


        self.checkBox.stateChanged.connect(self.statiChanged)

    def setValue(self, value):
        self.valueLabel.setText(value)

    def changeState(self):
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

    def mousePressEvent(self, QMouseEvent):
        self.changeState()

    def size(self):
        return QtCore.QSize(200, 50)

class ColouredRectangle(QtGui.QWidget):

    clicked = QtCore.pyqtSignal()

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
        self.clicked.emit()



class CheckBoxWithoutKeyPress(QtGui.QCheckBox):

    keyPressed = QtCore.pyqtSignal(object)

    def __init__(self):
        super(CheckBoxWithoutKeyPress, self).__init__()

    def keyPressEvent(self, qKeyEvent):
        self.keyPressed.emit(qKeyEvent)



class ClickableLabel(QtGui.QLabel):

    clicked = QtCore.pyqtSignal()

    def __init__(self):
        super(ClickableLabel, self).__init__()

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()