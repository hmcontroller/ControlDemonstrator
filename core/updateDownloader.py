# -*- encoding: utf-8 -*-
import timeit
import traceback
import urllib2
import os
import zipfile

from PyQt4 import QtCore


class UpdateDownloader(QtCore.QObject):

    workDone = QtCore.pyqtSignal(object)
    progress = QtCore.pyqtSignal(object)

    def __init__(self):
        super(UpdateDownloader, self).__init__()

        self.downloadUri = ""

        self.zipOutFileName = "microRayDownloadedUpdate.zip"
        self.zipFileTargetPath = ""

        self.zipExtractionFolderName = "extractedUpdate"
        self.zipExtractionFolderPath = ""

    @QtCore.pyqtSlot(object)
    def doWork(self, uriAndTargetFolder):
        startTime = timeit.default_timer()

        self.downloadUri = uriAndTargetFolder[0]
        self.zipFileTargetPath = os.path.join(uriAndTargetFolder[1], self.zipOutFileName)
        self.zipExtractionFolderPath = os.path.join(uriAndTargetFolder[1], self.zipExtractionFolderName)

        response = self.downloadZipFile(self.downloadUri)

        if response[0] is not None:
            self.extractZipFile()

        elapsed = timeit.default_timer() - startTime
        self.workDone.emit(response)

    def downloadZipFile(self, uri):
        response = tuple()
        CHUNK_SIZE = 16 * 1024

        if os.path.isdir(os.path.dirname(self.zipFileTargetPath)):
            pass
        else:
            os.makedirs(os.path.dirname(self.zipFileTargetPath))

        try:
            response = urllib2.urlopen(uri)
            with open(self.zipFileTargetPath, 'wb') as outFile:
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
        with zipfile.ZipFile(self.zipFileTargetPath, "r") as zipFile:
            zipFile.extractall(self.zipExtractionFolderPath)

        os.remove(self.zipFileTargetPath)

