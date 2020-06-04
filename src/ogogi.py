# TODO : Decorate all print thing

import os
import time
import datetime

import mysql.connector

# Modularized parts
import fileIO
import config
import compileScript
import gradingScript
import abb
import importlib
import sys

from colorama import Style, Fore, init  # Terminal decoration

ogogi_bare = abb.bold + Fore.YELLOW + "OGOGI" + Style.RESET_ALL
ogogi = "[ " + ogogi_bare + " ] "


def onRecieved(submission, probInfo):
    # Reassign for better readability
    resultID = submission[0]
    uploadTime = str(submission[1])
    userID = str(submission[2])
    probID = str(submission[3])
    inContest = submission[9]
    language = submission[10]

    print("Result ID :\t" + str(resultID))
    print(abb.bold + "Subject   :\t" + userID)
    print("Sub Time  :\t" + uploadTime)
    print(abb.bold + "Prob ID   :\t" + probID + Style.RESET_ALL)
    probName = str(probInfo[2])

    resultStr = ""
    sumTime = 0
    nCase = 0

    complieResult = None

    # Interprete subject source file name
    subjectFileName = config.subjectFileName
    _replaces = [("[probID]", probID), ("[uploadTime]", uploadTime)]
    for ph, rep in _replaces:
        subjectFileName = subjectFileName.replace(ph, rep)

    scriptPath = config.scriptPath.replace("[probName]", probName)

    if os.path.exists(scriptPath):
        # Unlimited # of testcase
        case: os.path = fileIO.read(scriptPath)
        nBegin = case.find(config.caseKey) + len(config.caseKey)
        nEnd = case.find(config.caseKeyEnd)
        nCase = int(case[nBegin:nEnd])

        print("nCase     :\t" + str(nCase), end="\n\n")
    else:
        complieResult = "NOCONFIG"

    # Compile subject's source file
    if complieResult == None:
        complieResult = compileScript.compile(subjectFileName, userID, language)

    # If there is no problem compiling, grade the subject.
    errmsg = ""
    if complieResult == None:
        print(abb.ok + "Subject's file successfully compiled.")
        if probInfo[8] and inContest:
            subtask = probInfo[8].split(" ")
        else:
            subtask = [nCase]
        resultStr, sumTime = gradingScript.run(submission, probInfo, subtask)
        # If grading script error (interactive)
        if sumTime == -1:
            complieResult == "INTERERR"
            errmsg = "Grading script error, contact admin."
            sumTime = 0

    # Compile error
    elif complieResult == "NOCMP":
        resultStr = "Compilation Error"
        print(abb.error + "Failed to compile subject's file.")
        # Try to read error message
        try:
            errmsg = fileIO.read("env/error.txt")
        except:
            print(abb.error + "Cannot read error log. Please check env/error.txt")
            errmsg = "Cannot read error log. Unknown problem occured."
    # File extension not supported
    elif complieResult == "NOLANG":
        resultStr = "Compilation Error"
        errmsg = "Language not supported. Please check file extension."
        print(abb.error + "Language not supported.")
    # Missing config file (config.cfg or script.php)
    elif complieResult == "NOCONFIG":
        resultStr = "Compilation Error"
        errmsg = "Cannot read config file. Please contact admins."
        print(abb.error + "script.php is missing.")

    # Calculate score
    percentage = 0
    roundedTime = 0
    if complieResult == None:
        print(abb.bold + "\nResult    :\t[" + abb.bold, end="")
        for e in resultStr:
            if e == "P":
                print(Fore.GREEN, end="")
            else:
                print(Fore.RED, end="")
            print(e, end="")
        print(Style.RESET_ALL + abb.bold + "]")
        # Count correct answer by counting 'P'
        nCorrect = resultStr.count("P")
        roundedTime = round(sumTime, 2)
        print("Time      :\t" + str(roundedTime) + " s" + Style.RESET_ALL)
        percentage = 100 * (nCorrect / nCase)

    return (resultStr, percentage, roundedTime, errmsg, resultID)


def main():
    # Decorative purpose.
    init()
    # Nope, this is not the real otog.cf password XD.
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="00000000",
        # Original for otog.cf was :
        # passwd='0000',
        database="OTOG",
    )

    myCursor = mydb.cursor(buffered=True)

    # for keybord interupt.
    print(ogogi + "Grader started. Waiting for submission...")

    while True:
        myCursor.execute("SELECT * FROM Result WHERE status = 0 ORDER BY time")
        submission = myCursor.fetchone()
        if submission != None:
            print(abb.bold + Fore.GREEN + "\t--> recieved.\n" + Style.RESET_ALL)
            print(
                str(datetime.datetime.now().strftime("[ %d/%m/%y %H:%M:%S ]"))
                + " -----------------------------"
            )

            myCursor.execute(
                "SELECT * FROM Problem WHERE id_Prob = " + str(submission[3])
            )
            probInfo = myCursor.fetchone()

            # Submit result
            sql = "UPDATE Result SET result = %s, score = %s, timeuse = %s, status = 1, errmsg = %s WHERE idResult = %s"
            val = onRecieved(submission, probInfo)
            myCursor.execute(sql, val)
            print("---------------------------------------------------")
            print("\n" + ogogi + "Finished grading session. Waiting for the next one.")

        mydb.commit()
        time.sleep(config.gradingInterval)


if __name__ == "__main__":
    main()
