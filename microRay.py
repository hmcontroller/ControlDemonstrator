# -*- encoding: utf-8 -*-
import sys
import traceback
import logging
from logging.handlers import RotatingFileHandler
import os
import time
import tempfile

from core.exceptHook import ExceptHook

from gui.splashScreen import SplashScreen

from PyQt4 import QtGui, QtCore


from gui.resources import *


if getattr(sys, 'frozen', False):
    # running from pyinstaller exe
    ROOT_FOLDER = sys._MEIPASS

    TEMP_FOLDER = os.path.join(tempfile.gettempdir(), "microRay")
    if not os.path.isdir(TEMP_FOLDER):
        os.makedirs(TEMP_FOLDER)

    SETTINGS_FOLDER = os.path.join(os.getenv('APPDATA'), "microRay")
    if not os.path.isdir(SETTINGS_FOLDER):
        os.makedirs(SETTINGS_FOLDER)
else:
    ROOT_FOLDER = os.path.dirname(os.path.realpath(__file__))
    TEMP_FOLDER = ROOT_FOLDER
    SETTINGS_FOLDER = ROOT_FOLDER




def getLogger():
    logFormatter = logging.Formatter('%(asctime)s %(levelname)-9s%(message)s')

    logFile = os.path.join(SETTINGS_FOLDER, 'mRay.log')

    my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=50*1024,
                                     backupCount=1, encoding=None, delay=0)
    my_handler.setFormatter(logFormatter)
    my_handler.setLevel(logging.INFO)

    LOGGER = logging.getLogger('root')
    LOGGER.setLevel(logging.INFO)
    LOGGER.addHandler(my_handler)

    return LOGGER





class ExceptionMagnet(QtCore.QObject):

    caughtException = QtCore.pyqtSignal(object)

    def __init__(self):
        super(ExceptionMagnet, self).__init__()
        self.logger = getLogger()

    def myExcepthook(self, exc_type, exc_value, exc_traceback):
        exc_string = ""
        for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
            exc_string += line
        self.logger.critical("uncaught exception:\n\n" + exc_string)
        self.caughtException.emit(exc_string)




class MicroRay(QtGui.QApplication):
    """
    Main entry point for the application.
    """
    def __init__(self, sysArgs, exceptionMagnet):

        self.logger = exceptionMagnet.logger
        self.logger.info("starting application")
        QtGui.QApplication.__init__(self, sysArgs)


        splashScreen = SplashScreen()

        splashScreen.show()
        QtGui.qApp.processEvents()
        QtGui.qApp.processEvents()

        splashScreen.setProgress(0.1)
        splashScreen.setMessage(u"importing libraries")
        QtGui.qApp.processEvents()

        from gui.mainWindow import MicroRayMainWindow

        splashScreen.setProgress(0.3)
        splashScreen.setMessage(u"loading main window")
        QtGui.qApp.processEvents()

        self.mainW = MicroRayMainWindow(exceptionMagnet,
                                        self.logger,
                                        ROOT_FOLDER,
                                        TEMP_FOLDER,
                                        SETTINGS_FOLDER,
                                        splashScreen)
        self.mainW.show()

    def notify(self, object, event):
        isex = False
        try:
            return QtGui.QApplication.notify(self, object, event)
        except:
            isex = True
            self.logger.error("uncaught exception:")
            self.logger.error(traceback.format_exc())
            return False
        finally:
            if isex:
                self.quit()


def run():
    exceptionMagnet = ExceptionMagnet()
    sys.excepthook = exceptionMagnet.myExcepthook

    app = MicroRay(sys.argv, exceptionMagnet)

    exitCode = app.exec_()
    sys.exit(exitCode)

if __name__ == "__main__":
    run()
