# -*- encoding: utf-8 -*-
import timeit
import traceback
import urllib2

from gui.constants import *

from PyQt4 import QtCore


class UpdateChecker(QtCore.QObject):

    workDone = QtCore.pyqtSignal(object)
    progress = QtCore.pyqtSignal(object)

    def __init__(self):
        super(UpdateChecker, self).__init__()

    @QtCore.pyqtSlot()
    def doWork(self):
        startTime = timeit.default_timer()

        response = tuple()

        try:
            response = urllib2.urlopen(MRAY_VERSION_FILE)
            versionNumberRaw = response.readline()
            pathToArchive = response.readline()
            actualVersionNumber = int(versionNumberRaw.replace("\n", "").replace("\r", ""))
            response = (actualVersionNumber, pathToArchive)
        except:
            response = (None, traceback.format_exc())


        elapsed = timeit.default_timer() - startTime
        self.workDone.emit(response)
