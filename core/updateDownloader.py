# -*- encoding: utf-8 -*-
import timeit
import traceback
import urllib2
import os
import zipfile
import distutils.dir_util


from gui.constants import *

from PyQt4 import QtCore


class UpdateDownloader(QtCore.QObject):

    workDone = QtCore.pyqtSignal(object)
    progress = QtCore.pyqtSignal(object)

    def __init__(self):
        super(UpdateDownloader, self).__init__()
        self.downloadUri = ""
        self.programRootFolder = ""
        self.zipOutFileName = "microRayDownload.zip"

    @QtCore.pyqtSlot(object)
    def doWork(self, uriAndProgramRootFolder):
        startTime = timeit.default_timer()

        self.downloadUri = uriAndProgramRootFolder[0]
        self.programRootFolder = uriAndProgramRootFolder[1]

        response = self.downloadZipFile(self.downloadUri)

        if response[0] is not None:
            self.extractZipFile()

        elapsed = timeit.default_timer() - startTime
        self.workDone.emit(response)

    def downloadZipFile(self, uri):
        response = tuple()
        CHUNK_SIZE = 16 * 1024

        try:
            response = urllib2.urlopen(uri)
            with open(self.zipOutFileName, 'wb') as outFile:
                while True:
                    chunk = response.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    outFile.write(chunk)

            response = (True, None)
        except:
            response = (None, traceback.format_exc())

        return response

    def extractZipFile(self):
        targetPath = ""
        with zipfile.ZipFile(self.zipOutFileName, "r") as zipFile:
            zipFile.extractall(targetPath)

        os.remove(os.path.join(self.programRootFolder, self.zipOutFileName))

    def replaceOldVersion(self):
        pathToExtractedFolder = os.path.join(self.programRootFolder, "microRay")

        try:
            distutils.dir_util.copy_tree(pathToExtractedFolder, self.programRootFolder)
        except:
            pass
