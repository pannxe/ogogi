import os
import execu
import config
import handler
import abb


def cmpFunc(fname1, fname2):
    f1 = open(fname1)
    f2 = open(fname2)

    f1_line = f1.readline()
    f2_line = f2.readline()

    while f1_line != "" or f2_line != "":
        f1_line = f1_line.rstrip()
        f2_line = f2_line.rstrip()
        if f1_line != f2_line:
            f1.close()
            f2.close()
            return False
        f1_line = f1.readline()
        f2_line = f2.readline()

    f1.close()
    f2.close()
    return True


def run(submission, probInfo, subtask):
    probName = str(probInfo[2])
    timeLimit = float(probInfo[4])
    memLimit = int(probInfo[5])
    timeLimit = float(probInfo[4])
    memLimit = int(probInfo[5])
    perfect = True
    lastTest = 0

    allResult = ""
    sumTime = 0

    uploadTime = str(submission[1])
    userID = str(submission[2])
    probID = str(submission[3])
    inContest = submission[9]
    language = submission[10]
    interacive_flag = False

    for sub in subtask:
        if inContest:
            allResult += "["
        if not perfect:
            for x in range(lastTest, int(sub)):
                allResult += "S"
            if inContest:
                allResult += "]"
            lastTest = int(sub)
            continue
        for x in range(lastTest, int(sub)):
            t, elapsedTime = execu.execute(
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
            solutionPath = config.solutionPath.replace("[probName]", probName).replace(
                "[#]", str(x + 1)
            )
            res = False
            if execResult == None and t == 0:
                # Interprete interactive_script.py path.
                interactivePath = config.interactivePath.replace("[probName]", probName)
                # If the problem is interacive...
                if os.path.exists(interactivePath + config.interactiveName):
                    if not interacive_flag:
                        print("\t--> This problem is interactive.")
                        interacive_flag = True
                    import sys

                    sys.path.insert(1, "./" + interactivePath)
                    import interactive_script

                    # Call interactive script.
                    res = interactive_script.cmp(resultPath, solutionPath)
                else:
                    res = cmpFunc(resultPath, solutionPath)
                if res:
                    allResult += "P"
                else:
                    perfect = False
                    allResult += "-"
            elif execResult == "TLE":
                allResult += "T"
                perfect = False
            else:
                allResult += "X"
                perfect = False
        if inContest:
            allResult += "]"
            lastTest = int(sub)
    return (allResult, sumTime)
