# -*- encoding: utf-8 -*-
from PyQt4 import QtGui, QtCore


class Gain(QtGui.QWidget):

    valueChanged = QtCore.pyqtSignal(float)

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.value = 0.6

        self.cablePen = QtGui.QPen()
        self.cablePen.setColor(QtGui.QColor(0, 0, 0))
        self.cablePen.setWidth(2)
        self.cablePen.setCosmetic(True)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFixedSize(100, 100)

        self.editor = GainEdit(parent=self)

        p = QtGui.QPalette()
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(QtGui.QColor(0,0,0,0)))
        self.editor.setStyleSheet("""border: none; background-color: rgba(0, 0, 0, 0);""")     #; margin-top: 8px """)
        self.editor.setPalette(p)
        self.editor.move(1, 16)
        self.editor.setText(str(self.value))

        self.editor.editingFinished.connect(self.editorChanged)

        self.path = QtGui.QPainterPath()
        self.path.moveTo(0, 0)
        self.path.lineTo(0, 60)
        self.path.lineTo(70, 30)
        self.path.closeSubpath()


    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Enter:
            self.editor.hide()

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(self.cablePen)
        painter.drawPath(self.path)

    def mouseDoubleClickEvent(self, QMouseEvent):
        self.editor.show()

    def editorChanged(self):
        try:
            self.value = float(self.editor.text().replace(",", "."))
        except:
            # TODO
            raise
        self.setFocus()
        self.editor.setText(str(self.value))
        self.update()
        self.valueChanged.emit(self.value)

    def confirmationTimeOut(self):
        print "hello gainWidget timeOut"

    def setValue(self, value):
        self.editor.setText(str(value))

    def getInCoordinates(self):
        return self.mapToGlobal(QtCore.QPoint(0, 30))

    def getTipCoordinates(self):
        return self.mapToGlobal(QtCore.QPoint(70, 30))


class GainEdit(QtGui.QLineEdit):
    def __init__(self, parent):
        QtGui.QLineEdit.__init__(self, parent)
        self.valueMin = 0
        self.valueMax = 1000
        self.valueDecimals = 10
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(50, self.height())
        self.setMaxLength(6)
        self.setFont(QtGui.QFont("sans-serif", 10))
        valli = QtGui.QRegExpValidator(QtCore.QRegExp("[-]{0,1}\d{0,}\.\d{0,}", QtCore.Qt.CaseInsensitive))
        self.setValidator(valli)
