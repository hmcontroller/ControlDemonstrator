# -*- encoding: utf-8 -*-
import sys
import traceback
import logging
import os

from PyQt4 import QtGui

from gui.mainWindow import ControlDemonstratorMainWindow
from commServers.udpServer import DataAquisitionServerUDP

logging.basicConfig(filename='log.log',
                    format='%(asctime)s %(levelname)-9s%(message)s',
                    level=logging.INFO)

ABSOLUTE_PROGRAM_ROOT_FOLDER = os.path.dirname(os.path.realpath(__file__))

# SERVER = DataAquisitionServerUDP()

def myExcepthook(exc_type, exc_value, exc_traceback):
    exc_string = ""
    for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
        exc_string += line
    logging.critical("uncaught exception:\n\n" + exc_string)
    # SERVER.stop()


class ControlDemonstrator(QtGui.QApplication):
    def __init__(self, args):
        logging.info("application start")
        QtGui.QApplication.__init__(self, args)

        self.mainW = ControlDemonstratorMainWindow(ABSOLUTE_PROGRAM_ROOT_FOLDER)
        self.mainW.show()

    def notify(self, object, event):
        isex = False
        try:
            return QtGui.QApplication.notify(self, object, event)
        except:
            isex = True
            logging.error("uncaught exception:")
            logging.error(traceback.format_exc())
            return False
        finally:
            if isex:
                self.quit()

    def stopServer(self):
        self.mainW.stopServer()


def run():
    # sys.excepthook = myExcepthook

    app = ControlDemonstrator(sys.argv)

    exitCode = app.exec_()
    app.stopServer()
    sys.exit(exitCode)

if __name__ == "__main__":
    run()
