# -*- encoding: utf-8 -*-
import sys
import traceback
import logging
from logging.handlers import RotatingFileHandler
import os

from core.exceptHook import ExceptHook

from PyQt4 import QtGui

from gui.mainWindow import ControlDemonstratorMainWindow

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




def myExcepthook(exc_type, exc_value, exc_traceback):
    exc_string = ""
    for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
        exc_string += line
    LOGGER.critical("uncaught exception:\n\n" + exc_string)
    print exc_string


class MicroRay(QtGui.QApplication):
    """
    Main entry point for the application.
    """
    def __init__(self, args):
        LOGGER.info("application start")
        QtGui.QApplication.__init__(self, args)

        self.excepthook = ExceptHook()
        # sys.excepthook = self.excepthook.hook


        self.mainW = ControlDemonstratorMainWindow(ABSOLUTE_PROGRAM_ROOT_FOLDER, self.excepthook)
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
    sys.excepthook = myExcepthook

    app = ControlDemonstrator(sys.argv)

    exitCode = app.exec_()
    sys.exit(exitCode)

if __name__ == "__main__":
    run()
