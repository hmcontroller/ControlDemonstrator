# -*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore


class IdColorLabelCheckbox(QtGui.QWidget):

    changed = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=None, id=None, color=None):
        super(IdColorLabelCheckbox, self).__init__(parent)
        self.id = id
        self.color = color

        horizontalLayout = QtGui.QHBoxLayout(self)
        horizontalLayout.setMargin(0)
        horizontalLayout.setSpacing(6)

        self.checkBox = QtGui.QCheckBox()
        self.colorBox = ColouredRectangle(self.color)
        self.label = QtGui.QLabel()

        horizontalLayout.addWidget(self.checkBox)
        horizontalLayout.addWidget(self.colorBox)
        horizontalLayout.addWidget(self.label)

        spacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        horizontalLayout.addItem(spacer)

        self.checkBox.stateChanged.connect(self.statiChanged)

    def statiChanged(self, state):
        self.changed.emit(self.id, state)

    def setText(self, text):
        self.label.setText(text)

    def setChecked(self, value):
        self.checkBox.setChecked(value)


class ColouredRectangle(QtGui.QWidget):
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


