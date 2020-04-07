# TODO : Decorate all print thing

import os
import time
import mysql.connector

# Modularized parts
import enum
import fileIO
import config
import subject
import handler

print('otogGrader 2.0.0')
print('*****Grader started*****')

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='0000',
    database='OTOG'
)


def cmpFunc(fname1, fname2):
    f1 = open(fname1)
    f2 = open(fname2)

    f1_line = f1.readline()
    f2_line = f2.readline()

    while f1_line != '' or f2_line != '':
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


def gradeSubject(submission, myCursor, mydb):
    # TODO : Move this shit to the new fuction (or new file).

    # Reassign for better readability
    uploadTime  = str(submission[1])
    resultID    = submission[0]
    userID      = str(submission[2])
    probID      = str(submission[3])
    inContest   = submission[9]
    fileLang    = submission[10]

    print('====================================')
    print(submission[:4])

    myCursor.execute('SELECT * FROM Problem WHERE id_Prob = ' + str(probID))
    probInfo    = myCursor.fetchone()

    probName    = str(probInfo[2])
    timeLimit   = float(probInfo[4])
    memLimit    = int(probInfo[5])

    cnt         = 0
    allResult   = ''
    perfect     = True
    sumTime     = 0
    lastTest    = 0
    nCase       = 0

    subjectFileName = config.subjectFileName.\
        replace('[probID]',     probID).\
        replace('[uploadTime]', uploadTime)

    result = subject.compile(subjectFileName, userID, fileLang)
    scriptPath = config.scriptPath.replace('[probName]', probName)

    if os.path.exists(scriptPath):
        case = fileIO.read(scriptPath)
        numStart = case.find(config.caseKey) + len(config.caseKey)
        numEnd = case.find(config.caseKeyEnd)
        # Unlimited # of testcase
        nCase = int(case[numStart:numEnd])
        print('# of testcase : ' + nCase)
    else:
        nCase = -1
        result = 'No Testcases.'

    if probInfo[8] and inContest:
        subtask = probInfo[8].split(' ')
    else:
        subtask = [nCase]

    if(result == None):
        for sub in subtask:
            if inContest:
                allResult += '['
            if not perfect:
                for x in range(lastTest, int(sub)):
                    allResult += 'S'
                if inContest:
                    allResult += ']'
                lastTest = int(sub)
                continue
            for x in range(lastTest, int(sub)):
                result = None
                t, elapsedTime = subject.execute(
                    fileLang, userID, probName, probID,
                    str(x + 1), timeLimit, 1024*memLimit, uploadTime
                )
                result = handler.runtimeHandler(t)
                sumTime += elapsedTime

                resultPath = config.resultPath
                solutionPath = config.solutionPath.\
                    replace('[probName]', probName).\
                    replace('[#]', str(x + 1))

                if(result == None and t == 0):
                    if(cmpFunc(resultPath, solutionPath)):
                        allResult += 'P'
                        cnt += 1
                    else:
                        perfect = False
                        allResult += '-'
                elif(result == 'TLE'):
                    allResult += 'T'
                    perfect = False
                else:
                    allResult += 'X'
                    perfect = False

                sql = 'UPDATE Result SET result = %s WHERE idResult = %s'
                val = ('Running in testcase #' + str(x+1), resultID)
                myCursor.execute(sql, val)
                mydb.commit()

            if inContest:
                allResult += ']'
            lastTest = int(sub)
    try:
        errmsg = fileIO.read('env/error.txt')
    except:
        errmsg = 'Something went wrong.'

    print('TIME : ' + str(sumTime))
    percentage = (cnt / nCase) * 100

    sql = 'UPDATE Result SET result = %s, score = %s, timeuse = %s, status = 1, errmsg = %s WHERE idResult = %s'
    val = (allResult, percentage, round(sumTime, 2), errmsg, resultID)
    myCursor.execute(sql, val)
    mydb.commit()


while True:
    myCursor = mydb.cursor(buffered=True)
    myCursor.execute('SELECT * FROM Result WHERE status = 0 ORDER BY time')
    submission = myCursor.fetchone()
    if(submission != None):
        gradeSubject(submission, myCursor, mydb)
    mydb.commit()
    time.sleep(1)
