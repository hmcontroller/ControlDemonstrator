# -*- encoding: utf-8 -*-

import os
import distutils.dir_util
import subprocess
import sys
import traceback
import time
import shutil

if getattr(sys, 'frozen', False):
    # running from pyinstaller exe
    ROOT_FOLDER = sys._MEIPASS

else:
    ROOT_FOLDER = None

# ROOT_FOLDER = os.path.dirname(os.path.realpath(__file__))

def run(pathToExtractedUpdateFolder, targetDirectory):

    print u"Applying microRay update."
    print u"Download is at {}".format(pathToExtractedUpdateFolder)
    print u"microRay is installed at {}".format(targetDirectory)

    # prevent overwriting myself here
    pathToDownloadedInstallerExe = os.path.join(pathToExtractedUpdateFolder, "ucomplete.exe")
    os.remove(pathToDownloadedInstallerExe)
    print u"removed {}".format(pathToDownloadedInstallerExe)

    print u"waiting for 3 seconds..."
    time.sleep(3)
    print u"start copying"
    distutils.dir_util.copy_tree(pathToExtractedUpdateFolder, targetDirectory)
    print u"copying complete"


    # start microRay
    exePath = os.path.join(targetDirectory, "microRay.exe")
    print u"starting {}".format(exePath)
    print subprocess.Popen(exePath)

    # remove extracted files
    shutil.rmtree(pathToExtractedUpdateFolder)
    print u"removed {}".format(pathToExtractedUpdateFolder)

if __name__ == "__main__":
    if ROOT_FOLDER is None:
        print "no root folder, good by."
    else:
        try:
            if len(sys.argv) > 2:
                pathToExtractedUpdateFolder = sys.argv[1]
                targetDirectory = sys.argv[2]
                try:
                    run(pathToExtractedUpdateFolder, targetDirectory)
                except:
                    errorFilePath = os.path.join(pathToExtractedUpdateFolder, "updateError.txt")
                    with open(errorFilePath, "w") as f:
                        f.write(traceback.format_exc())
            else:
                workingDirectory = ""
                targetDirectory = ""
                time.sleep(3)
                try:
                    run(workingDirectory, targetDirectory)
                except:
                    errorFilePath = os.path.join(workingDirectory, "updateError.txt")
                    with open(errorFilePath, "w") as f:
                        f.write(traceback.format_exc())
        except:
            print traceback.format_exc()

    userInput = raw_input(u"Bitte Taste drücken, um Fenster zu schließen.")