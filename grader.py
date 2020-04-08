# TODO : Decorate all print thing

import os
import time

# For local debugging
import localDebugger as mysql
# import mysql.connector

# Modularized parts
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


def gradeSubject(submission, myCursor):
    # TODO : Move this shit to the new fuction (or new file).

    # Reassign for better readability
    resultID    = submission[0]
    uploadTime  = str(submission[1])
    userID      = str(submission[2])
    probID      = str(submission[3])
    inContest   = submission[9]
    language    = submission[10]

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

    # Interprete subject source file name
    subjectFileName = config.subjectFileName.\
        replace('[probID]',     probID).\
        replace('[uploadTime]', uploadTime)

    # Compile subject's source file
    result = subject.compile(subjectFileName, userID, language)

    # Interprete config file
    case = ''
    nBegin = 0
    nEnd = 0
    # For compatibity with legacy 'script.php' from otog.org era.
    legacyPath = config.legacyScriptPath.replace('[probName]', probName)
    # otogGrader 2.0 now uses 'config.cfg' instead.
    configPath = config.configPath.replace('[probName]', probName)
    
    if os.path.exists(legacyPath):
        case = fileIO.read(legacyPath)
        nBegin = case.find(config.legacyCaseKey) + len(config.legacyCaseKey)
        nEnd = case.find(config.legacyCaseKeyEnd)
    elif os.path.exists(configPath):
        case = fileIO.read(configPath)
        nBegin = case.find(config.caseKey) + len(config.caseKey)
        nEnd = case.find(config.caseKeyEnd)
    else:
        result = 'NOCONFIG'

    # If no error reading config file, print number of case to console
    if result != 'NOCONFIG':
        # Unlimited # of testcase
        nCase = int(case[nBegin:nEnd])
        print('# of testcase : ' + nCase)

    # If there is no problem compiling, grade the subject.
    if result == None :
        print('Subject\'s file successfully compiled.')
        if probInfo[8] and inContest :
            subtask = probInfo[8].split(' ')
        else :
            subtask = [nCase]
        if os.path.exists('script.py') :
            print('Interactive script enabled. Running ...')
            # -----------------------
            # TODO Interactive stuff
            # -----------------------
        else:
            # TODO Move this thing to another file
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
                        language, userID, probName, probID,
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
        # End else
    # Compile error
    elif result == 'NOCMP' :
        print('Error: Failed to compile subject\'s file.')
        # Try to read error message
        try :
            errmsg = fileIO.read('env/error.txt')
        except :
            errmsg = 'Cannot read error log. Unknown problem occured.'
    # File extension not supported
    elif result == 'NOLANG' :
        errmsg = 'Language not supported. Please check file extension.'
        print('Error: Language not supported.')
    # Missing config file (config.cfg or script.php)
    elif result == 'NOCONFIG' :
        errmsg = 'Cannot read config file. Please contact admins.'
        print('Error: config.cfg or script.php is missing.')


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
    if(submission != None) :
        gradeSubject(submission, myCursor)
    else :
        print('Error : submission from SQL = None')
    mydb.commit()
    time.sleep(1)
