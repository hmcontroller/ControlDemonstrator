# -*- encoding: utf-8 -*-
import sys
import traceback
import logging
import os

from core.exceptHook import ExceptHook

from PyQt4 import QtGui

from gui.mainWindow import ControlDemonstratorMainWindow

logging.basicConfig(filename='log.log',
                    format='%(asctime)s %(levelname)-9s%(message)s',
                    level=logging.INFO)


ABSOLUTE_PROGRAM_ROOT_FOLDER = os.path.dirname(os.path.realpath(__file__))


def myExcepthook(exc_type, exc_value, exc_traceback):
    exc_string = ""
    for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
        exc_string += line
    logging.critical("uncaught exception:\n\n" + exc_string)


class ControlDemonstrator(QtGui.QApplication):
    """
    Main entry point for the application.
    """
    def __init__(self, args):
        logging.info("application start")
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
            logging.error("uncaught exception:")
            logging.error(traceback.format_exc())
            return False
        finally:
            if isex:
                self.quit()


def run():
    # sys.excepthook = myExcepthook

    app = ControlDemonstrator(sys.argv)

    exitCode = app.exec_()
    sys.exit(exitCode)

if __name__ == "__main__":
    run()
