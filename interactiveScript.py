import handler
import config
import subject
import abb
import os
import fileIO
import subprocess


def callScript(**kwargs):
    configPath = config.interactiveCfgPath.replace("[probName]", kwargs["probName"])
    answerPath = config.interactiveAnsPath.replace("[probName]", kwargs["probName"])
    scriptPath = config.interactivePath.replace("[probName]", kwargs["probName"])
    if os.path.exists(configPath):
        os.system("chmod 777 " + configPath)
        os.system("rm " + configPath)
    if os.path.exists(answerPath):
        os.system("chmod 777 " + answerPath)
        os.system("rm " + answerPath)

    # Surely needed to be fixed

    fileIO.write(configPath, str(kwargs))
    cmd = "python3 " + scriptPath + "; exit;"

    subprocess.Popen([cmd], shell=True, preexec_fn=os.setsid)

    buffer = fileIO.read(answerPath)

    # Process buffer
    correctKey = buffer.find(config.interactiveResultKey) + len(
        config.interactiveResultKey
    )
    correctKeyEnd = buffer.find(config.interactiveKeyEnd, correctKey)
    correct = buffer[correctKey:correctKeyEnd]

    timeKey = buffer.find(config.interactiveTimeKey) + len(config.interactiveTimeKey)
    timeKeyEnd = buffer.find(config.interactiveKeyEnd, timeKey)
    elapsedTime = int(buffer[timeKey:timeKeyEnd])

    errKey = buffer.find(config.interactiveErrorKey) + len(config.interactiveErrorKey)
    errKeyEnd = buffer.find(config.interactiveKeyEnd, errKey)
    t = buffer[errKey:errKeyEnd]

    correct = False
    elapsedTime = 0

    return correct, t, elapsedTime


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
            correct, t, elapsedTime = callScript(
                language=language,
                userID=userID,
                probName=probName,
                probID=probID,
                atCase=str(x + 1),
                timeLimit=timeLimit,
                memLimit=(1024 * memLimit),
                uploadTime=uploadTime,
            )

            execResult = handler.runtimeHandler(t)
            sumTime += elapsedTime

            if execResult == None and t == 0:
                if correct:
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
