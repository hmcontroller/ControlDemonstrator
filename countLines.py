import os

ownPath = os.path.dirname(os.path.abspath(__file__))
ownName = os.path.basename(os.path.abspath(__file__))
print "ownPath", ownPath, "ownName", ownName

allInterestingFiles = []
counter = 0

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
    #print allInterestingFiles

def count(withoutComments=False):
    print

    counter = 0

    for aPath in allInterestingFiles:
        counterPerFile = 0
        with open(aPath, "r") as f:
            for line in f:
                if line == "":
                    continue
                if withoutComments:
                    if line.strip().startswith("#"):
                        continue
                counter += 1
                counterPerFile += 1
        print "count {} -> {}".format(aPath, counterPerFile)
    return counter



def run():
    iterateFolders(ownPath)
    print "found {} lines.".format(count(withoutComments=True))
    try:
        input("Press Enter to close...")
    except:
        pass
    print "bye"


if __name__ == "__main__": run()