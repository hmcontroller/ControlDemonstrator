import os

ownPath = os.path.dirname(os.path.abspath(__file__))
ownName = os.path.basename(os.path.abspath(__file__))
print "ownPath", ownPath, "ownName", ownName


allInterestingFiles = []

def iterateFolders(path):
    allFiles = os.listdir(path)
    for aFileName in allFiles:
        filePath = os.path.join(path, aFileName)
        if os.path.isdir(filePath):
            if not filePath.endswith("designerfiles") and \
               not filePath.endswith(".git") and \
               not filePath.endswith(".idea") and \
               not filePath.endswith("testSnippets") and \
               not filePath.endswith("sphinx") and \
               not filePath.endswith("pyqtgraph") and \
               not filePath.endswith("documentation") and \
               not filePath.endswith("dist") and \
               not filePath.endswith("build"):
                print "diving into {}".format(filePath)
                iterateFolders(filePath)
        if filePath == os.path.join(ownPath, ownName):
            continue
        if not filePath.endswith(".py"):
            continue
        allInterestingFiles.append(filePath)

def count():
    print

    counter = 0
    blankLinesCounter = 0
    commentsCounter = 0
    fileCounter = 0

    insideBlockComment = False

    for aPath in allInterestingFiles:
        counterPerFile = 0
        with open(aPath, "r") as f:
            fileCounter += 1
            for line in f:
                if line.strip() == "":
                    blankLinesCounter += 1
                if line.strip().startswith("#"):
                    commentsCounter += 1
                if line.strip().startswith('"""'):
                    insideBlockComment = True
                    commentsCounter += 1
                if insideBlockComment is True:
                    commentsCounter += 1
                if line.strip().endswith('"""'):
                    insideBlockComment = False
                if insideBlockComment is False:
                    counter += 1
                    counterPerFile += 1
        print "count {} -> {}".format(aPath, counterPerFile)
    return counter, blankLinesCounter, commentsCounter, fileCounter



def run():
    iterateFolders(ownPath)
    counter, blankLinesCounter, commentsCounter, fileCounter = count()
    print
    print "{} files".format(fileCounter)
    print "{} lines of code".format(counter)
    print "{} lines with comments".format(commentsCounter)
    print "{} blank lines".format(blankLinesCounter)
    print "{} total lines".format(counter + blankLinesCounter + commentsCounter)
    print "{:.1f} code lines per file".format(float(counter) / float(fileCounter))
    print "\nThank you, byebye."
    # try:
    #     input("Press Enter to close...")
    # except:
    #     pass


if __name__ == "__main__": run()