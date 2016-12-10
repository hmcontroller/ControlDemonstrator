# -*- encoding: utf-8 -*-
import os, time
import datetime
import operator as dictop

from PyQt4 import QtCore, QtGui, QtSql

from gui.designerfiles.main_window import Ui_MainWindow


#import settings as settings

print os.path.dirname(os.path.abspath(__file__))



class ControlDemonstratorMainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        splashImagePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Regelkreis.gif")
        splashMap = QtGui.QPixmap(splashImagePath)
        splashScreen = QtGui.QSplashScreen(splashMap)
        splashScreen.show()
        QtGui.qApp.processEvents()
        splashScreen.showMessage(u"Regulator wird geladen...", QtCore.Qt.AlignCenter)
        QtGui.qApp.processEvents()


        #time.sleep(3)

        splashScreen.finish(self)


        self.myControllerClass = MyController()
        self.verticalLayout_2.insertWidget(0, self.myControllerClass, 0)

        self.myPlotterClass = MyPlotter()
        self.horizontalLayout_3.insertWidget(0, self.myPlotterClass, 0)


class MyController(QtGui.QGraphicsView):

    clickController = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        #self.setHorizontalScrollBarPolicy(1)
        #self.setVerticalScrollBarPolicy(1)

        self.setStyleSheet("""
            .MyController {
                border-style: none;
                }
            """)


        # ganzes fixe Zeug zeichnen

        self.scene = QtGui.QGraphicsScene()

        cablePen = QtGui.QPen()
        cablePen.setColor(QtGui.QColor(0, 0, 0))
        cablePen.setWidth(5)
        cablePen.setCosmetic(True)

        inPointMarkLineObject = QtCore.QLineF(100, 200, 300, 200)
        self.inPointMarkLine = self.scene.addLine(inPointMarkLineObject, cablePen)

        self.scene.setSceneRect(0, 0, self.width(), self.height())
        self.setScene(self.scene)


    def resizeEvent(self, QResizeEvent):
        self.emit(QtCore.SIGNAL("resize()"))

    def mousePressEvent(self, QMouseEvent):
        self.clickController.emit(QMouseEvent.x(), QMouseEvent.y())




class MyPlotter(QtGui.QGraphicsView):

    clickPlot = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        #self.setHorizontalScrollBarPolicy(1)
        #self.setVerticalScrollBarPolicy(1)




    def resizeEvent(self, QResizeEvent):
        self.emit(QtCore.SIGNAL("resize()"))

    def mousePressEvent(self, QMouseEvent):
        self.clickPlot.emit(QMouseEvent.x(), QMouseEvent.y())


