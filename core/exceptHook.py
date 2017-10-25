# -*- encoding: utf-8 -*-

import traceback
import logging

from PyQt4 import QtCore

class ExceptHook(QtCore.QObject):

    caughtException = QtCore.pyqtSignal(object)

    def __init__(self):
        super(ExceptHook, self).__init__()

    def hook(self, exc_type, exc_value, exc_traceback):
        exc_string = ""
        for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
            exc_string += line
        logging.critical("uncaught exception:\n\n" + exc_string)
        self.caughtException.emit(exc_string)
        print exc_string