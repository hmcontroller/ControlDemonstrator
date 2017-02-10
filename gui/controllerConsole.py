# -*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from gui.graphicItems.commandWidgets.gain import Gain
from gui.graphicItems.commandWidgets.switch import Switch
from gui.graphicItems.gauges.tankGauge import TankGauge
from gui.graphicItems.symbols.arrow import Arrow
from gui.graphicItems.symbols.sumCircle import SumCircle





class MyController(QtGui.QGraphicsView):

    parameterChanged = QtCore.pyqtSignal(int, float)

    def __init__(self, commandList, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        self.setHorizontalScrollBarPolicy(1)
        self.setVerticalScrollBarPolicy(1)

        self.commands = commandList

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(False)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.simulate)

        self.setStyleSheet("""
            .MyController {
                border-style: none;
                }
            """)

        self.scene = QtGui.QGraphicsScene()

        # ganzes fixe Zeug zeichnen


        cablePen = QtGui.QPen()
        cablePen.setColor(QtGui.QColor(0, 0, 0))
        cablePen.setWidth(2)
        cablePen.setCosmetic(True)

        testLine = QtCore.QLineF(100, 200, 300, 200)
        self.testLine = self.scene.addLine(testLine, cablePen)

        self.arrow = Arrow()
        self.scene.addItem(self.arrow)
        #self.arrow.setFillColor(QtGui.QColor(0, 0, 0))
        #self.arrow.setRotation(75)
        self.arrow.setPos(QtCore.QPointF(300, 200))

        self.sumCircle1 = SumCircle()
        self.scene.addItem(self.sumCircle1)
        self.sumCircle1.setPos(QtCore.QPointF(335, 200))


        self.tankWidget0 = TankGauge()
        self.tankProxy0 = self.scene.addItem(self.tankWidget0)
        self.tankWidget0.setPos(400, 150)
        self.tankWidget0.setLevel(0)
        self.tankWidget0.setColor(QtGui.QBrush(QtGui.QColor(230, 0, 0)))

        self.tankWidget1 = TankGauge()
        self.tankProxy1 = self.scene.addItem(self.tankWidget1)
        self.tankWidget1.setPos(500, 150)
        self.tankWidget1.setLevel(0)
        self.tankWidget1.setColor(QtGui.QBrush(QtGui.QColor(0, 150, 0)))

        self.tankWidget2 = TankGauge()
        self.tankProxy2 = self.scene.addItem(self.tankWidget2)
        self.tankWidget2.setPos(600, 150)
        self.tankWidget2.setLevel(0)
        self.tankWidget2.setColor(QtGui.QBrush(QtGui.QColor(0, 153, 255)))

        self.tankWidget3 = TankGauge()
        self.tankProxy3 = self.scene.addItem(self.tankWidget3)
        self.tankWidget3.setPos(700, 150)
        self.tankWidget3.setLevel(0)
        self.tankWidget3.setColor(QtGui.QBrush(QtGui.QColor(255, 165, 0)))

        gainCommand = None
        for cmd in self.commands:
            if cmd.name == "SLOW_PWM_PERCENT":
                gainCommand = cmd

        self.gainWidget = Gain()
        self.gainWidget.setValue(gainCommand.value)
        self.gainProxy2 = self.scene.addWidget(self.gainWidget)
        self.gainProxy2.setPos(400, 300)
        self.gainWidget.valueChanged.connect(gainCommand.setValue)
        gainCommand.confirmationTimeOut.connect(self.gainWidget.confirmationTimeOut)
        gainOut = self.gainWidget.getTipCoordinates()


        switchCommand = None
        for cmd in self.commands:
            if cmd.name == "SLOW_PWM_ON":
                switchCommand = cmd

        self.switch = Switch()
        self.switch.setOn(gainCommand.value)
        self.scene.addItem(self.switch)
        self.switch.setPos(QtCore.QPointF(580, 330))
        switchIn = self.switch.getSwitchInCoordinates()
        self.switch.valueChanged.connect(switchCommand.setValue)
        switchCommand.confirmationTimeOut.connect(self.switch.confirmationTimeOut)

        self.scene.addLine(QtCore.QLineF(gainOut, switchIn), cablePen)

        self.scene.setSceneRect(0, 0, self.width(), self.height())
        self.setScene(self.scene)

    def simulate(self):
        if self.levelRising is True:
            self.tankLevel += 1
        else:
            self.tankLevel -= 1
        if self.tankLevel > 100:
            self.levelRising = False
            self.tankLevel = 100
        if self.tankLevel < 0:
            self.levelRising = True
            self.tankLevel = 0

        self.tankWidget.setLevel(self.tankLevel)
        self.scene.update()

    def resizeEvent(self, QResizeEvent):
        self.emit(QtCore.SIGNAL("resize()"))
        self.scene.setSceneRect(0, 0, self.width(), self.height())

    # def mousePressEvent(self, QMouseEvent):
    #     self.clickController.emit(QMouseEvent.x(), QMouseEvent.y())

    def itemValueChanged(self, parameterNumber, value):
        self.parameterChanged.emit(parameterNumber, value)