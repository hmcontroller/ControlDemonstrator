# -*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from core.signalGeneratorCommandGroup import SignalGeneratorCommandGroup

from gui.graphicItems.commandWidgets.gain import Gain
from gui.graphicItems.commandWidgets.switch import Switch
from gui.graphicItems.gauges.tankGauge import TankGauge
from gui.graphicItems.symbols.arrow import Arrow

from gui.graphicItems.symbols.sumCircle import SumCircle
from gui.graphicItems.commandWidgets.signalGenerator import SignalGenerator
from gui.graphicItems.symbols.derivativeFunction import DerivativeFunctionBlock
from gui.graphicItems.symbols.integralFunction import IntegralFunctionBlock
from gui.graphicItems.symbols.distributionNode import DistributionNode
from gui.graphicItems.symbols.corner import Corner
from gui.graphicItems.commandWidgets.gaugeSwitcher import GaugeSwitcher


class ControllerWaterLineExperiment(QtGui.QGraphicsView):

    parameterChanged = QtCore.pyqtSignal(int, float)

    def __init__(self, commands, channels, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        # self.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.lightGray))

        # self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.commands = commands
        self.channels = channels

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(False)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.simulate)

        self.setStyleSheet("""
            .ControllerWaterLineExperiment {
                border-style: none;
                }
            """)

        self.scene = QtGui.QGraphicsScene()

        self.cablePen = QtGui.QPen()
        self.cablePen.setColor(QtGui.QColor(0, 0, 0))
        self.cablePen.setWidth(2)
        self.cablePen.setCosmetic(True)


        sigCommandGroup = SignalGeneratorCommandGroup()
        sigCommandGroup.functionNumberCommand = self.commands.getCommandByName("SP_GEN1_NUMBER")
        sigCommandGroup.diracNowCommand = self.commands.getCommandByName("SP_GEN1_DIRAC_NOW")
        sigCommandGroup.diracLowCommand = self.commands.getCommandByName("SP_GEN1_DIRAC_LOW")
        sigCommandGroup.diracHighCommand = self.commands.getCommandByName("SP_GEN1_DIRAC_HIGH")
        sigCommandGroup.diracDurationCommand = self.commands.getCommandByName("SP_GEN1_DIRAC_DURATION")
        sigCommandGroup.stepLowCommand = self.commands.getCommandByName("SP_GEN1_STEP_LOW")
        sigCommandGroup.stepHighCommand = self.commands.getCommandByName("SP_GEN1_STEP_HIGH")
        sigCommandGroup.stepStateCommand = self.commands.getCommandByName("SP_GEN1_STEP_STATE")
        sigCommandGroup.sinAmplitudeCommand = self.commands.getCommandByName("SP_GEN1_SIN_AMPLITUDE")
        sigCommandGroup.sinOmegaCommand = self.commands.getCommandByName("SP_GEN1_SIN_OMEGA")
        sigCommandGroup.sinOffsetCommand = self.commands.getCommandByName("SP_GEN1_SIN_OFFSET")
        sigCommandGroup.squareLowCommand = self.commands.getCommandByName("SP_GEN1_SQUARE_LOW")
        sigCommandGroup.squareHighCommand = self.commands.getCommandByName("SP_GEN1_SQUARE_HIGH")
        sigCommandGroup.squareFrequencyCommand = self.commands.getCommandByName("SP_GEN1_SQUARE_FREQUENCY")
        sigCommandGroup.rampState = self.commands.getCommandByName("SP_GEN1_RAMP_STATE")
        sigCommandGroup.rampGradient = self.commands.getCommandByName("SP_GEN1_RAMP_GRADIENT")
        sigCommandGroup.rampLow = self.commands.getCommandByName("SP_GEN1_RAMP_LOW")
        sigCommandGroup.rampHigh = self.commands.getCommandByName("SP_GEN1_RAMP_HIGH")

        signalGenerator = SignalGenerator(sigCommandGroup)
        self.scene.addItem(signalGenerator)
        signalGenerator.setPos(10, 150)


        sumCircleControllerIn = SumCircle()
        self.scene.addItem(sumCircleControllerIn)
        sumCircleControllerIn.setPos(235, 200)


        nodeControllerIn = DistributionNode()
        self.scene.addItem(nodeControllerIn)
        nodeControllerIn.setPos(300, 200)


        proportionalGainCommand = self.commands.getCommandByName("PID1_KP_VALUE")

        proportionalGain = Gain(proportionalGainCommand)
        self.scene.addItem(proportionalGain)
        proportionalGain.setPos(350, 70)


        proportionalSwitchCommand = self.commands.getCommandByName("PID1_KP_SWITCH")

        proportionalSwitch = Switch(proportionalSwitchCommand)
        self.scene.addItem(proportionalSwitch)
        proportionalSwitch.setPos(550, 100)


        derivativeGainCommand = self.commands.getCommandByName("PID1_KD_VALUE")
        derivativeGain = Gain(derivativeGainCommand)
        self.scene.addItem(derivativeGain)
        derivativeGain.setPos(350, 170)


        derivativeSwitchCommand = self.commands.getCommandByName("PID1_KD_SWITCH")

        derivativeSwitch = Switch(derivativeSwitchCommand)
        self.scene.addItem(derivativeSwitch)
        derivativeSwitch.setPos(550, 200)


        integrativeGainCommand = self.commands.getCommandByName("PID1_KI_VALUE")
        integrativeGain = Gain(integrativeGainCommand)
        self.scene.addItem(integrativeGain)
        integrativeGain.setPos(350, 270)

        integrativeSwitchCommand = self.commands.getCommandByName("PID1_KI_SWITCH")

        integrativeSwitch = Switch(integrativeSwitchCommand)
        self.scene.addItem(integrativeSwitch)
        integrativeSwitch.setPos(550, 300)


        distCommandGroup = SignalGeneratorCommandGroup()
        distCommandGroup.functionNumberCommand = self.commands.getCommandByName("SP_GEN2_NUMBER")
        distCommandGroup.diracNowCommand = self.commands.getCommandByName("SP_GEN2_DIRAC_NOW")
        distCommandGroup.diracLowCommand = self.commands.getCommandByName("SP_GEN2_DIRAC_LOW")
        distCommandGroup.diracHighCommand = self.commands.getCommandByName("SP_GEN2_DIRAC_HIGH")
        distCommandGroup.diracDurationCommand = self.commands.getCommandByName("SP_GEN2_DIRAC_DURATION")
        distCommandGroup.stepLowCommand = self.commands.getCommandByName("SP_GEN2_STEP_LOW")
        distCommandGroup.stepHighCommand = self.commands.getCommandByName("SP_GEN2_STEP_HIGH")
        distCommandGroup.stepStateCommand = self.commands.getCommandByName("SP_GEN2_STEP_STATE")
        distCommandGroup.sinAmplitudeCommand = self.commands.getCommandByName("SP_GEN2_SIN_AMPLITUDE")
        distCommandGroup.sinOmegaCommand = self.commands.getCommandByName("SP_GEN2_SIN_OMEGA")
        distCommandGroup.sinOffsetCommand = self.commands.getCommandByName("SP_GEN2_SIN_OFFSET")
        distCommandGroup.squareLowCommand = self.commands.getCommandByName("SP_GEN2_SQUARE_LOW")
        distCommandGroup.squareHighCommand = self.commands.getCommandByName("SP_GEN2_SQUARE_HIGH")
        distCommandGroup.squareFrequencyCommand = self.commands.getCommandByName("SP_GEN2_SQUARE_FREQUENCY")
        distCommandGroup.rampState = self.commands.getCommandByName("SP_GEN2_RAMP_STATE")
        distCommandGroup.rampGradient = self.commands.getCommandByName("SP_GEN2_RAMP_GRADIENT")
        distCommandGroup.rampLow = self.commands.getCommandByName("SP_GEN2_RAMP_LOW")
        distCommandGroup.rampHigh = self.commands.getCommandByName("SP_GEN2_RAMP_HIGH")

        disturbanceGenerator = SignalGenerator(distCommandGroup)
        self.scene.addItem(disturbanceGenerator)
        disturbanceGenerator.setPos(800, 10)
        # disturbanceGenerator.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)

        disturbanceOnOffCommand = self.commands.getCommandByName("SP_GEN2_ON")
        disturbanceSwitch = Switch(disturbanceOnOffCommand)
        self.scene.addItem(disturbanceSwitch)
        disturbanceSwitch.setPos(725, 100)
        disturbanceSwitch.rotate(90)

        disturbanceOnOffCommand.value = 0.0
        # alternativ geht auch
        # disturbanceSwitch.setValue(0.0)

        duDt = DerivativeFunctionBlock()
        self.scene.addItem(duDt)
        duDt.setPos(450, 175)


        integrator = IntegralFunctionBlock()
        self.scene.addItem(integrator)
        integrator.setPos(450, 275)


        sumCircleControllerOut = SumCircle()
        self.scene.addItem(sumCircleControllerOut)
        sumCircleControllerOut.setPos(650, 200)
        # sumCircleControllerOut.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)

        sumCircleDisturbance = SumCircle()
        self.scene.addItem(sumCircleDisturbance)
        sumCircleDisturbance.setPos(725, 200)


        gauges = list()

        tankGaugeChannel1 = self.channels.getChannelByName("SP_GEN_1_OUTPUT")
        tankGauge1 = TankGauge()
        tankGauge1.lowerLimit = 0.1
        tankGauge1.upperLimit = 0.9
        tankGauge1.isRelativeScale = True
        tankGauge1.setColor(tankGaugeChannel1.colorRgbTuple)
        tankGaugeChannel1.newValueArrived.connect(tankGauge1.newValueArrived)
        gauges.append(tankGauge1)

        tankGaugeChannel2 = self.channels.getChannelByName("ANALOG_IN_2")
        tankGauge2 = TankGauge()
        tankGauge2.lowerLimit = 0
        tankGauge2.upperLimit = 1
        tankGauge2.isRelativeScale = True
        tankGauge2.setColor(tankGaugeChannel2.colorRgbTuple)
        tankGaugeChannel2.newValueArrived.connect(tankGauge2.newValueArrived)
        gauges.append(tankGauge2)

        gaugeSwitchCommand = self.commands.getCommandByName("PID1_SENSOR_SOURCE")

        gaugeSwitcher = GaugeSwitcher(gaugeSwitchCommand, gauges)
        self.scene.addItem(gaugeSwitcher)
        gaugeSwitcher.setPos(790, 235)

        nodeOut = DistributionNode()
        self.scene.addItem(nodeOut)
        nodeOut.setPos(830, 200)


        cornerPointPropGain = self.addCorner(300, 100)
        cornerPointIntegralGain = self.addCorner(300, 300)
        cornerPointPropSwitch = self.addCorner(650, 100)
        cornerPointIntegralSwitch = self.addCorner(650, 300)
        cornerPointSumControllerIn = self.addCorner(235, 400)
        cornerPointSensorOut = self.addCorner(830, 400)
        cornerDisturber = self.addCorner(725, 60)






        ###########################################################################
        #############   from here on only lines and arrows are drawn  #############
        ###########################################################################






        self.drawLine(nodeControllerIn.coordinates, cornerPointPropGain.coordinates)
        self.drawLine(cornerPointPropGain.coordinates, proportionalGain.inCoordinates)

        self.drawLine(sumCircleControllerIn.eastCoordinates, nodeControllerIn.coordinates)
        self.drawLine(nodeControllerIn.coordinates, derivativeGain.inCoordinates)

        self.drawLine(derivativeGain.outCoordinates, duDt.westCoordinates)
        self.drawLine(duDt.eastCoordinates, derivativeSwitch.inCoordinates)

        self.drawLine(integrativeGain.outCoordinates, integrator.westCoordinates)
        self.drawLine(integrator.eastCoordinates, integrativeSwitch.inCoordinates)

        self.drawLine(proportionalGain.outCoordinates, proportionalSwitch.inCoordinates)

        self.drawLine(nodeControllerIn.coordinates, cornerPointIntegralGain.coordinates)
        self.drawLine(cornerPointIntegralGain.coordinates, integrativeGain.inCoordinates)

        self.drawLine(proportionalSwitch.outCoordinates, cornerPointPropSwitch.coordinates)
        self.drawArrow(cornerPointPropSwitch.coordinates, sumCircleControllerOut.northCoordinates)

        self.drawArrow(derivativeSwitch.outCoordinates, sumCircleControllerOut.westCoordinates)

        self.drawLine(integrativeSwitch.outCoordinates, cornerPointIntegralSwitch.coordinates)
        self.drawArrow(cornerPointIntegralSwitch.coordinates, sumCircleControllerOut.southCoordinates)

        self.drawArrow(signalGenerator.eastCoordinates, sumCircleControllerIn.westCoordinates)

        self.drawArrow(cornerPointSumControllerIn.coordinates, sumCircleControllerIn.southCoordinates)
        self.drawLine(cornerPointSumControllerIn.coordinates, cornerPointSensorOut.coordinates)

        self.drawLine(cornerPointSensorOut.coordinates, gaugeSwitcher.southCoordinates)

        self.drawArrow(sumCircleControllerOut.eastCoordinates, sumCircleDisturbance.westCoordinates)

        self.drawLine(sumCircleDisturbance.eastCoordinates, nodeOut.coordinates)

        # the output signal
        self.drawArrow(nodeOut.coordinates, QtCore.QPointF(1000, 200))

        self.drawArrow(nodeOut.coordinates, gaugeSwitcher.northCoordinates)

        self.drawLine(disturbanceGenerator.westCoordinates, cornerDisturber.coordinates)
        self.drawLine(cornerDisturber.coordinates, disturbanceSwitch.inCoordinates)
        self.drawArrow(disturbanceSwitch.outCoordinates, sumCircleDisturbance.northCoordinates)

        # the minus sign
        self.drawLine(QtCore.QPointF(245, 225), QtCore.QPointF(250, 225))






        # self.scene.setSceneRect(0, 0, self.width(), self.height())
        self.setScene(self.scene)

    def addCorner(self, x, y):
        corner = Corner()
        corner.setPos(x, y)
        return corner

    def drawLine(self, start, end):
        self.scene.addLine(QtCore.QLineF(start, end), self.cablePen)

    def drawArrow(self, start, end):
        arrow = Arrow(start, end)
        self.scene.addItem(arrow)
        arrow.setPos(start)

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

        self.tankWidget.setValue(self.tankLevel)
        self.scene.update()

    def updateSymbols(self):
        self.scene.update()

    def resizeEvent(self, QResizeEvent):
        super(ControllerWaterLineExperiment, self).resizeEvent(QResizeEvent)
        # self.scene.setSceneRect(0, 0, self.width(), self.height())
