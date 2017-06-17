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


def run(pathToExtractedUpdateFolder, targetDirectory):

    print u"Applying microRay update..."
    # print u"Download is at {}".format(pathToExtractedUpdateFolder)
    # print u"microRay is installed at {}".format(targetDirectory)

    # prevent overwriting myself here
    pathToDownloadedInstallerExe = os.path.join(pathToExtractedUpdateFolder, "ucomplete1.exe")
    try:
        os.remove(pathToDownloadedInstallerExe)
        # print u"removed {}".format(pathToDownloadedInstallerExe)
    except:
        pass

    print u"start copying new files..."

    # print u"waiting for 3 seconds to allow the gui to close... (don't tell the user)"
    time.sleep(3)

    distutils.dir_util.copy_tree(pathToExtractedUpdateFolder, targetDirectory)
    print u"copying complete."


    # start microRay
    exePath = os.path.join(targetDirectory, "microRay.exe")
    print u"starting microRay..."
    subprocess.Popen(exePath)

    # remove extracted files
    shutil.rmtree(pathToExtractedUpdateFolder)
    print u"removed {}".format(pathToExtractedUpdateFolder)
    print u"Good bye."


if __name__ == "__main__":
    if ROOT_FOLDER is None:
        print u"Error 'no root folder', unable to update."
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
                # for debugging only
                workingDirectory = u""
                targetDirectory = u""
                time.sleep(3)
                try:
                    run(workingDirectory, targetDirectory)
                except:
                    errorFilePath = os.path.join(workingDirectory, "updateError.txt")
                    with open(errorFilePath, "w") as f:
                        f.write(traceback.format_exc())
        except:
            print traceback.format_exc()

    # das geht irgendwie nicht
    # userInput = raw_input(u"Bitte Taste drücken, um Fenster zu schließen.")