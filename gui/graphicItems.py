from PyQt4 import QtCore, QtGui, QtSql

class MyArrow(QtGui.QGraphicsItem):
    def __init__(self):
        QtGui.QGraphicsItem.__init__(self)
        # self.pen = QtGui.QPen()
        # self.pen.setColor(QtGui.QColor(0, 0, 0))
        # self.pen.setWidth(1)
        # self.pen.setCosmetic(True)
        self.painterPath = QtGui.QPainterPath()
        self.painterPath.moveTo(-5, -5)
        self.painterPath.lineTo(20, 0)
        self.painterPath.lineTo(-5, 5)
        self.painterPath.lineTo(0, 0)
        self.painterPath.closeSubpath()
        self.painterPath.setFillRule(QtCore.Qt.WindingFill)
        self.brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.fillPath(self.painterPath, self.brush)
        #QPainter.drawPath(self.painterPath)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 10)

    def setFillColor(self, color):
        self.brush.setColor(color)
        self.update()


class MySumCircle(QtGui.QGraphicsItem):
    def __init__(self):
        QtGui.QGraphicsItem.__init__(self)
        self.width = 30
        self.height = 30

        self.painterPath = QtGui.QPainterPath()
        self.painterPath.addEllipse(QtCore.QPointF(0, 0), self.width/2, self.height/2)
        # self.painterPath.setFillRule(QtCore.Qt.WindingFill)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        #QPainter.fillPath(self.painterPath, self.brush)
        QPainter.drawPath(self.painterPath)

    def boundingRect(self):
        return QtCore.QRectF(-self.width/2, -self.height/2, self.width/2, self.height/2)

    def setWidthHeight(self, width, height):
        self.width = width
        self.height = height


class MySwitch(QtGui.QGraphicsObject):

    valueChanged = QtCore.pyqtSignal(int, float)

    def __init__(self, command=None):
        QtGui.QGraphicsObject.__init__(self)

        self.command = command

        self.setAcceptHoverEvents(True)
        self.showBoundingRect = False
        self.bounds = [-20, -20, 50, 20]
        self.height = 30
        self.isOn = True
        self.brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))

        self.painterPath = QtGui.QPainterPath()
        self.painterPath.addEllipse(QtCore.QPointF(0, 0), 3, 3)
        self.painterPath.addEllipse(QtCore.QPointF(30, 0), 3, 3)
        self.painterPath.setFillRule(QtCore.Qt.WindingFill)

        self.normalPen = QtGui.QPen()
        self.normalPen.setColor(QtGui.QColor(0, 0, 0))
        self.normalPen.setCosmetic(True)
        self.normalPen.setWidth(2)


        self.dottedPen = QtGui.QPen()
        self.dottedPen.setStyle(QtCore.Qt.DashLine)
        self.dottedPen.setCosmetic(True)
        self.dottedPen.setWidth(1)

        self.painterPath1 = QtGui.QPainterPath()
        self.painterPath1.moveTo(-10, 0)
        self.painterPath1.lineTo(0, 0)
        self.painterPath1.lineTo(30, 0)
        self.painterPath1.moveTo(30, 0)
        self.painterPath1.lineTo(40, 0)

        self.boundingRectPath = QtGui.QPainterPath()
        self.boundingRectPath.moveTo(self.bounds[0], self.bounds[1])
        self.boundingRectPath.lineTo(self.bounds[2], self.bounds[1])
        self.boundingRectPath.lineTo(self.bounds[2], self.bounds[3])
        self.boundingRectPath.lineTo(self.bounds[0], self.bounds[3])
        self.boundingRectPath.closeSubpath()



    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        #print self.painterPath
        if self.isOn is True:
            self.painterPath1.setElementPositionAt(2, 30, 0)
        else:
            self.painterPath1.setElementPositionAt(2, 23, -15)
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        QPainter.fillPath(self.painterPath, self.brush)

        QPainter.setPen(self.normalPen)
        QPainter.drawPath(self.painterPath1)

        if self.showBoundingRect is True:
            QPainter.setPen(self.dottedPen)
            QPainter.drawPath(self.boundingRectPath)

    def boundingRect(self):
        return QtCore.QRectF(self.bounds[0], self.bounds[1], self.bounds[2] - self.bounds[0], self.bounds[3] - self.bounds[1])

    def setWidthHeight(self, width, height):
        self.width = width
        self.height = height

    def setOn(self, on):
        self.isOn = on

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        if self.isOn is True:
            self.setOn(False)
        else:
            self.setOn(True)
        QtGui.QGraphicsItem.mousePressEvent(self, QGraphicsSceneMouseEvent)
        self.valueChanged.emit(self.command.id, self.isOn)

    def hoverEnterEvent(self, QGraphicsSceneMouseEvent):
        self.showBoundingRect = True
        QtGui.QGraphicsItem.hoverEnterEvent(self, QGraphicsSceneMouseEvent)

    def hoverLeaveEvent(self, QGraphicsSceneMouseEvent):
        self.showBoundingRect = False
        QtGui.QGraphicsItem.hoverLeaveEvent(self, QGraphicsSceneMouseEvent)


class MyGain(QtGui.QGraphicsItem):
    def __init__(self):
        QtGui.QGraphicsItem.__init__(self)
        self.setAcceptHoverEvents(True)
        self.showBoundingRect = False
        self.bounds = [-20, -20, 50, 20]
        self.height = 80
        self.width = 80
        self.brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))


        # self.dottedPen = QtGui.QPen()
        # self.dottedPen.setStyle(QtCore.Qt.DashLine)

        self.painterPath1 = QtGui.QPainterPath()
        self.painterPath1.moveTo(0, 0)
        self.painterPath1.lineTo(0, -self.height/2)
        self.painterPath1.lineTo(self.width, 0)
        self.painterPath1.lineTo(0, self.height/2)
        self.painterPath1.closeSubpath()

        # self.boundingRectPath = QtGui.QPainterPath()
        # self.boundingRectPath.moveTo(self.bounds[0], self.bounds[1])
        # self.boundingRectPath.lineTo(self.bounds[2], self.bounds[1])
        # self.boundingRectPath.lineTo(self.bounds[2], self.bounds[3])
        # self.boundingRectPath.lineTo(self.bounds[0], self.bounds[3])
        # self.boundingRectPath.closeSubpath()

        self.textItem = QtGui.QGraphicsTextItem(parent=self)
        self.textItem.setPlainText("Guckstdu")
        self.textItem.setPos(-10, 10)
        self.textItem.setTextInteractionFlags(QtCore.Qt.TextEditable)


        #proxy = self.scene().addWidget(QtGui.QLineEdit())



    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        # #print self.painterPath
        # if self.isOn is True:
        #     self.painterPath1.setElementPositionAt(2, 30, 0)
        # else:
        #     self.painterPath1.setElementPositionAt(2, 23, -15)
        QPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        # QPainter.fillPath(self.painterPath, self.brush)
        # QPainter.setPen(QtGui.QPen())
        QPainter.drawPath(self.painterPath1)
        # if self.showBoundingRect is True:
        #     QPainter.setPen(self.dottedPen)
        #     QPainter.drawPath(self.boundingRectPath)

    def boundingRect(self):
        return QtCore.QRectF(0, -self.height/2, self.width, self.height/2)

    def setWidthHeight(self, width, height):
        self.width = width
        self.height = height

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        QtGui.QGraphicsItem.mousePressEvent(self, QGraphicsSceneMouseEvent)

    def hoverEnterEvent(self, QGraphicsSceneMouseEvent):
        self.showBoundingRect = True
        QtGui.QGraphicsItem.hoverEnterEvent(self, QGraphicsSceneMouseEvent)

    def hoverLeaveEvent(self, QGraphicsSceneMouseEvent):
        self.showBoundingRect = False
        QtGui.QGraphicsItem.hoverLeaveEvent(self, QGraphicsSceneMouseEvent)


class MyTankGauge(QtGui.QGraphicsItem):
    def __init__(self):
        QtGui.QGraphicsItem.__init__(self)

        self.level = -50

        self.width = 20
        self.height = -100

        self.tankBorder = QtGui.QPainterPath()
        self.tankBorder.addRect(0, 0, self.width, self.height)

        self.fillRect = QtGui.QPainterPath()
        self.fillRect.moveTo(0, 0)
        self.fillRect.lineTo(self.width, 0)
        self.fillRect.lineTo(self.width, self.level)
        self.fillRect.lineTo(0, self.level)
        self.fillRect.closeSubpath()

        self.digitBorder = QtGui.QPainterPath()
        self.digitBorder.moveTo(self.width + 5, self.level)
        self.digitBorder.lineTo(self.width + 10, self.level - 10)
        self.digitBorder.lineTo(self.width + 40, self.level - 10)
        self.digitBorder.lineTo(self.width + 40, self.level + 10)
        self.digitBorder.lineTo(self.width + 10, self.level + 10)
        self.digitBorder.closeSubpath()

        self.black = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        self.tankColor = QtGui.QBrush(QtGui.QColor(0, 153, 255))

        self.textRect = QtCore.QRectF(self.width + 10, self.level + 10, self.width + 40, self.level - 10)

    def reposition(self):
        self.digitBorder.setElementPositionAt(0, self.width + 1, self.level)
        self.digitBorder.setElementPositionAt(1, self.width + 10, self.level - 10)
        self.digitBorder.setElementPositionAt(2, self.width + 40, self.level - 10)
        self.digitBorder.setElementPositionAt(3, self.width + 40, self.level + 10)
        self.digitBorder.setElementPositionAt(4, self.width + 10, self.level + 10)
        self.digitBorder.setElementPositionAt(5, self.width + 1, self.level)
        self.fillRect.setElementPositionAt(2, self.width, self.level)
        self.fillRect.setElementPositionAt(3, 0, self.level)
        self.textRect = QtCore.QRectF(self.width + 10, self.level - 10, 28, 20)

    def paint(self, painter, QStyleOptionGraphicsItem, QWidget_widget=None):
        self.reposition()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawPath(self.tankBorder)
        painter.fillPath(self.tankBorder, QtGui.QColor(240, 240, 240))
        # for i in range(1, 5):
        #     painter.drawLine(0, -i*25, self.width, -i*25)
        painter.fillPath(self.fillRect, self.tankColor)
        painter.drawPath(self.digitBorder)
        painter.fillPath(self.digitBorder, QtGui.QColor(240, 240, 240))
        painter.setFont(QtGui.QFont("Sans Serif", 12))
        painter.drawText(self.textRect,
                         QtCore.Qt.AlignRight or QtCore.Qt.AlignVCenter,
                         QtCore.QString(str(self.level * -1)))

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 70, 110)

    def setColor(self, color):
        self.tankColor = color
        self.update()

    def setLevel(self, value):
        self.level = int(value * -1)
        self.reposition()
        self.update()



class MyPlotLinePart(QtGui.QGraphicsItem):
    def __init__(self, points):
        QtGui.QGraphicsItem.__init__(self)
        self.points = points
        self.painterPath = QtGui.QPainterPath()

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        if len(self.points) > 0:
            self.painterPath.moveTo(self.points[0])
            for point in self.points:
                self.painterPath.lineTo(point)
        #QPainter.setRenderHint(QtGui.QPainter.Antialiasing)

        QPainter.drawPath(self.painterPath)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 10)

class MyPlotGroup(QtGui.QGraphicsObject):
    def __init__(self, points, color):
        QtGui.QGraphicsObject.__init__(self)
        self.points = points
        self.color = color
        self.plotLines = []
        for i in range(0, 5):
            self.plotLines.append(MyPlotLinePart(self.points))

        self.pen = QtGui.QPen()
        self.pen.setColor(self.color)
        self.pen.setWidth(2)
        self.pen.setCosmetic(True)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        QPainter.setPen(self.pen)
        for line in self.plotLines:
            line.paint(QPainter, QStyleOptionGraphicsItem, QWidget_widget=None)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 25, 10)


class MyLineEditWidget(QtGui.QWidget):

    valueChanged = QtCore.pyqtSignal(int, float)

    def __init__(self, command):
        QtGui.QWidget.__init__(self)

        self.command = command


        self.cablePen = QtGui.QPen()
        self.cablePen.setColor(QtGui.QColor(0, 0, 0))
        self.cablePen.setWidth(2)
        self.cablePen.setCosmetic(True)

        #self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setFixedSize(100, 100)
        self.editor = MyGainEdit(parent=self)
        p = QtGui.QPalette()
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(QtGui.QColor(0,0,0,0)))
        self.editor.setStyleSheet("""border: none; background-color: rgba(0, 0, 0, 0);""")     #; margin-top: 8px """)
        self.editor.setPalette(p)
        self.editor.move(1, 16)
        self.value = 0.6
        self.editor.setText(str(self.value))
        # self.editor.setFont(QtGui.QFont("sans-serif", 12))
        # valli = QtGui.QDoubleValidator(self.valueMin, self.valueMax, self.valueDecimals)
        # self.editor.setValidator(valli)

        self.editor.editingFinished.connect(self.editorChanged)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Enter:
            self.editor.hide()
        #super(QtGui.QWidget, self).keyPressEvent(QKeyEvent)


    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter()
        path = QtGui.QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(0, 60)
        path.lineTo(70, 30)
        path.closeSubpath()
        painter.begin(self)
        painter.setPen(self.cablePen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.drawPath(path)

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
        self.valueChanged.emit(self.command.id, self.value)



class MyGainEdit(QtGui.QLineEdit):
    def __init__(self, parent):
        QtGui.QLineEdit.__init__(self, parent)
        self.valueMin = 0
        self.valueMax = 1000
        self.valueDecimals = 10
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(50, self.height())
        self.setMaxLength(6)
        self.setFont(QtGui.QFont("sans-serif", 10))
        #valli = QtGui.QDoubleValidator(self.valueMin, self.valueMax, self.valueDecimals)
        valli = QtGui.QRegExpValidator(QtCore.QRegExp("[-]{0,1}\d{0,}\.\d{0,}", QtCore.Qt.CaseInsensitive))
        self.setValidator(valli)
        #self.setFrame(False) no effect


