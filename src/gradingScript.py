import os
import executeScript
import config
import handler
import abb
from compareEqual import *


def run(submission, probInfo, subtask):
    probName = str(probInfo[2])
    timeLimit = float(probInfo[4])
    memLimit = int(probInfo[5])
    timeLimit = float(probInfo[4])
    memLimit = int(probInfo[5])
    perfect = True
    lastTest = 0

    resultStr = ""
    sumTime = 0

    uploadTime = str(submission[1])
    userID = str(submission[2])
    probID = str(submission[3])
    inContest = submission[9]
    language = submission[10]
    isInteracive = False

    for sub in subtask:
        if inContest:
            resultStr += "["
        if not perfect:
            for x in range(lastTest, int(sub)):
                resultStr += "S"
            if inContest:
                resultStr += "]"
            lastTest = int(sub)
            continue
        for x in range(lastTest, int(sub)):
            t, elapsedTime = executeScript.execute(
                language,
                userID,
                probName,
                probID,
                str(x + 1),
                timeLimit,
                1024 * memLimit,
                uploadTime,
            )
            execResult = handler.runtimeHandler(t)
            sumTime += elapsedTime

            resultPath = config.resultPath

            solutionPath = config.solutionPath
            _replaces = [("[probName]", probName), ("[#]", str(x + 1))]
            for ph, rep in _replaces:
                solutionPath = solutionPath.replace(ph, rep)

            res = False
            if execResult == None and t == 0:
                # Interprete interactive_script.py path.
                interactivePath = config.interactivePath.replace("[probName]", probName)
                # If the problem is interacive...
                if os.path.exists(interactivePath + config.interactiveName):
                    if not isInteracive:
                        print("\t--> This problem is interactive.")
                        isInteracive = True
                    import sys

                    sys.path.insert(1, "./" + interactivePath)
                    try:
                        import interactive_script

                        # Call interactive script.
                        res = interactive_script.cmp(resultPath, solutionPath)
                    except:
                        print(abb.error + "Cannot import interactive script.\n\t--> Abort")
                else:
                    res = compareEqual(resultPath, solutionPath)
                if res:
                    resultStr += "P"
                else:
                    perfect = False
                    resultStr += "-"
            elif execResult == "TLE":
                resultStr += "T"
                perfect = False
            else:
                resultStr += "X"
                perfect = False
        if inContest:
            resultStr += "]"
            lastTest = int(sub)
    return (resultStr, sumTime)
