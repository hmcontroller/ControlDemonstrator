# -*- encoding: utf-8 -*-
import sys
import traceback
import logging
from logging.handlers import RotatingFileHandler
import os

from core.exceptHook import ExceptHook

from PyQt4 import QtGui, QtCore

from gui.mainWindow import MicroRayMainWindow

ABSOLUTE_PROGRAM_ROOT_FOLDER = os.path.dirname(os.path.realpath(__file__))

logFormatter = logging.Formatter('%(asctime)s %(levelname)-9s%(message)s')

logFile = os.path.join(ABSOLUTE_PROGRAM_ROOT_FOLDER, 'log.log')

my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024,
                                 backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(logFormatter)
my_handler.setLevel(logging.INFO)

LOGGER = logging.getLogger('root')
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(my_handler)



# logging.basicConfig(filename='log.log',
#                     format='%(asctime)s %(levelname)-9s%(message)s',
#                     level=logging.INFO)



class ExceptionMagnet(QtCore.QObject):

    caughtException = QtCore.pyqtSignal(object)

    def __init__(self):
        super(ExceptionMagnet, self).__init__()

    def myExcepthook(self, exc_type, exc_value, exc_traceback):
        exc_string = ""
        for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
            exc_string += line
        LOGGER.critical("uncaught exception:\n\n" + exc_string)
        self.caughtException.emit(exc_string)


class MicroRay(QtGui.QApplication):
    """
    Main entry point for the application.
    """
    def __init__(self, sysArgs, exceptionMagnet):
        LOGGER.info("application start")

        QtGui.QApplication.__init__(self, sysArgs)

        self.mainW = MicroRayMainWindow(ABSOLUTE_PROGRAM_ROOT_FOLDER, sysArgs, exceptionMagnet)
        self.mainW.show()

    def notify(self, object, event):
        isex = False
        try:
            return QtGui.QApplication.notify(self, object, event)
        except:
            isex = True
            LOGGER.error("uncaught exception:")
            LOGGER.error(traceback.format_exc())
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
