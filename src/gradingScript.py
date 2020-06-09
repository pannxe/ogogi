import os
import executeScript
import config
import handler
import abb
from compareEqual import compareEqual


def run(submission, probInfo, subtask, mydb):
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
            mycursor = mydb.cursor(buffered=True)
            sql = "UPDATE Result SET result = %s WHERE idResult = %s"
            val = ("Running in testcase " + str(x + 1), submission[0])
            mycursor.execute(sql, val)
            mydb.commit()

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
                interactivePath = config.interactivePath.replace(
                    "[probName]", probName)
                # If the problem is interacive...
                if os.path.exists(interactivePath):
                    if not isInteracive:
                        print("\t--> This problem is interactive.")
                        isInteracive = True
                    import subprocess

                    # Call interactive script.
                    try:
                        interactive_script = subprocess.Popen(
                            [
                                "python3",
                                interactivePath,
                                resultPath,
                                config.problemDirectory.replace(
                                    "[probName]", probName),
                                str(x + 1),
                            ],
                            stdout=subprocess.PIPE,
                        )
                        stdout = (
                            interactive_script.communicate(
                            )[0].decode("UTF-8").strip()
                        )
                        res = True if stdout == "P" else False
                    except:
                        print(
                            abb.error
                            + "Cannot grade using interactive script.\n\t--> Abort"
                        )
                        return ("Grading Script Error", -1)
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
