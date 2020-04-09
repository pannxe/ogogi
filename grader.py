# TODO : Decorate all print thing

import os
import time

import mysql.connector

# Modularized parts
import fileIO
import config
import subject
import standardScript
import interactiveScript
import otogEnum
import cmdMode
from kbhit import KBHit
from colorama import Style, Fore, init


def gradeSubject(submission, probInfo):
    # TODO : Move this shit to the new fuction (or new file).

    # Reassign for better readability
    resultID = submission[0]
    uploadTime = str(submission[1])
    userID = str(submission[2])
    probID = str(submission[3])
    inContest = submission[9]
    language = submission[10]

    print("Result ID :\t" + str(resultID))
    print("Subject   :\t" + userID)
    print("Prob ID   :\t" + probID)
    print("Sub Time  :\t" + uploadTime)
    probName = str(probInfo[2])

    allResult = ""
    sumTime = 0
    nCase = 0

    # Interprete subject source file name
    subjectFileName = config.subjectFileName.replace("[probID]", probID).replace(
        "[uploadTime]", uploadTime
    )

    scriptPath = config.scriptPath.replace("[probName]", probName)

    if os.path.exists(scriptPath):
        # Unlimited # of testcase
        case = fileIO.read(scriptPath)
        nBegin = case.find(config.caseKey) + len(config.caseKey)
        nEnd = case.find(config.caseKeyEnd)
        nCase = int(case[nBegin:nEnd])

        print("nCase     :\t" + str(nCase), end='\n\n')
    else:
        result = "NOCONFIG"

    # Compile subject's source file
    result = subject.compile(subjectFileName, userID, language)

    # If there is no problem compiling, grade the subject.
    errmsg = ""
    if result == None:
        print(otogEnum.ok + "Subject's file successfully compiled.")
        if probInfo[8] and inContest:
            subtask = probInfo[8].split(" ")
        else:
            subtask = [nCase]
        if os.path.exists(config.interactivePath):
            print("Interactive script enabled. Running ...")
            allResult, sumTime = interactiveScript.run(
                config.interactivePath, submission, probInfo, subtask
            )
        else:
            # run standard script
            allResult, sumTime = standardScript.run(submission, probInfo, subtask)
        if inContest:
            allResult += "]"
    # Compile error
    elif result == "NOCMP":
        allResult = "Compilation Error"
        print(otogEnum.error + "Failed to compile subject's file.")
        # Try to read error message
        try:
            errmsg = fileIO.read("env/error.txt")
        except:
            errmsg = "Cannot read error log. Unknown problem occured."
    # File extension not supported
    elif result == "NOLANG":
        allResult = "Compilation Error"
        errmsg = "Language not supported. Please check file extension."
        print(otogEnum.error + "Language not supported.")
    # Missing config file (config.cfg or script.php)
    elif result == "NOCONFIG":
        allResult = "Compilation Error"
        errmsg = "Cannot read config file. Please contact admins."
        print(otogEnum.error + "config.cfg or script.php is missing.")

    percentage = 0
    if result == None:
        print("\nResult    :\t[" + otogEnum.bold, end="")
        for e in allResult:
            if e == "P":
                print(Fore.GREEN, end="")
            else:
                print(Fore.RED, end="")
            print(e, end="")
        print(Style.RESET_ALL + "]")
        # Count correct answer by counting 'P'
        nCorrect = allResult.count("P")
        print("Time      :\t" + str(round(sumTime, 2)) + ' s')
        percentage = 100 * (nCorrect / nCase)

    return (allResult, percentage, round(sumTime, 2), errmsg, resultID)


if __name__ == "__main__":
    # Decorative purpose
    init()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="00000000",
        # Original for otog.cf was :
        # passwd='0000',
        database="OTOG",
    )

    flaged = False
    myCursor = mydb.cursor(buffered=True)

    # for keybord interupt.
    kb = KBHit()
    print("OGOGI started")
    while True:
        # Looking for keyboard interupt.
        if kb.kbhit():
            c = kb.getch()
            if c == ':':
                # Do function
                print('Keyboard interupted. Entering command mode.')
                kb.set_normal_term()
                cmd = cmdMode.run()
                # Shutdown signal
                if cmd == 1:
                    break
                kb.set_kbhit_term()
                print('Command mode exited.')
        
        myCursor.execute("SELECT * FROM Result WHERE status = 0 ORDER BY time")
        submission = myCursor.fetchone()
        if submission != None:
            print("=============================================")
            print(Fore.GREEN + "Submission recieved." + Style.RESET_ALL)
            flaged = False

            myCursor.execute(
                "SELECT * FROM Problem WHERE id_Prob = " + str(submission[3])
            )
            probInfo = myCursor.fetchone()

            # Submit result
            sql = "UPDATE Result SET result = %s, score = %s, timeuse = %s, status = 1, errmsg = %s WHERE idResult = %s"
            val = gradeSubject(submission, probInfo)
            myCursor.execute(sql, val)
            print("=============================================\n")

        elif not flaged:
            print("Waiting for submission...\n")
            flaged = True
        mydb.commit()
        time.sleep(config.gradingInterval)
    print("OGOGI : Bye")
