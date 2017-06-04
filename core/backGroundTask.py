# -*- encoding: utf-8 -*-

from PyQt4 import QtCore



class BackgroundTask(QtCore.QObject):

    startWorkSig = QtCore.pyqtSignal(object)
    progressSig = QtCore.pyqtSignal(object)
    workDoneSig = QtCore.pyqtSignal(object)
    threadStartedSignal = QtCore.pyqtSignal(QtCore.QThread)
    threadFinishedSignal = QtCore.pyqtSignal(QtCore.QThread)

    def __init__(self, worker, workDoneHandler, progressHandler=None):
        super(BackgroundTask, self).__init__()
        self.thread = None
        self.worker = None
        self.workerClass = worker

        self.workDoneSig.connect(workDoneHandler)

        self.progressHandler = progressHandler
        if progressHandler is not None:
            self.progressSig.connect(progressHandler)

        self.isWorking = False


    def startWork(self, workInfo=None):
        if self.thread is not None:
            raise Exception("Task in progress")
        self.thread = QtCore.QThread()
        self.worker = self.workerClass()
        self.worker.moveToThread(self.thread)
        self.startWorkSig.connect(self.worker.doWork)
        self.worker.workDone.connect(self.workDone)
        self.worker.workDone.connect(self.thread.quit)
        if self.progressHandler is not None:
            self.worker.progress.connect(self.progressReport)

        self.isWorking = True
        self.thread.start()
        self.threadStartedSignal.emit(self.thread)
        self.startWorkSig.emit(workInfo)


    def progressReport(self, progressInfo):
        if self.progressHandler is not None:
            self.progressSig.emit(progressInfo)

    def workDone(self, result):
        self.threadFinishedSignal.emit(self.thread)
        self.isWorking = False
        self.thread.quit()
        self.workDoneSig.emit(result)
        self.thread = None
