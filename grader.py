# TODO : Decorate all print thing

import os
import signal
import time
import subprocess
import codecs
import mysql.connector

# Modularized parts
import enum
import config
import fileIO

print('otogGrader 2.0.0')
print('*****Grader started*****')

mydb = mysql.connector.connect(
    host        = 'localhost',
    user        = 'root',
    passwd      = '0000',
    database    = 'OTOG'
)

def cmpFunc(fname1, fname2):
    f1      = open(fname1)
    f2      = open(fname2)

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


while True:
    myCursor = mydb.cursor(buffered=True)
    myCursor.execute(
        'SELECT * FROM Result WHERE status = 0 ORDER BY time'
    )
    submission = myCursor.fetchone()
    if(submission != None):
        # TODO : Move this shit to the new fuction (or new file).

        # Reassign for better readability
        uploadTime  = str(submission[1])
        userID      = str(submission[2])
        probID      = str(submission[3])
        contestMode = submission[9]
        fileLang    = submission[10]
        probName    = str(probInfo[2])
        timeLimit   = float(probInfo[4])
        memLimit    = int(probInfo[5])


        print('====================================')
        print(submission[:4])

        myCursor.execute(
            'SELECT * FROM Problem WHERE id_Prob = ' + str(probID)
        )
        probInfo = myCursor.fetchone()

        cnt         = 0
        ans         = ''
        perfect     = True
        sumTime     = 0
        lastTest    = 0
        result      = None

        result = subject.compile(probID + '_' + uploadTime, userID, fileLang)

        if(os.path.exists('source/' + probName + '/script.php')):
            case      = fileIO.read('source/' + probName + '/script.php')
            idx       = case.find('cases = ')
            testcase  = ''
            testcase  = testcase + case[idx + 8]

            if(case[idx + 9] != ';'): 
                testcase += case[idx + 9]
            print('Testcase : ' + testcase)
        else :
            testcase  =  '-1'
            result    =  'No Testcases.'

        if probInfo[8] and contestMode : 
            subtask = probInfo[8].split(' ')
        else : 
            subtask = [testcase]

        if(result == None):
            for sub in subtask:
                if contestMode : 
                    ans += '['
                if perfect == False:
                    for x in range(lastTest, int(sub)):
                        ans += 'S'
                    if contestMode :
                        ans += ']'
                    lastTest = int(sub)
                    continue
                for x in range(lastTest, int(sub)):
                    result = None
                    t, elapsedTime = subject.execute(
                        fileLang, userID, probName, probID,
                        str(x + 1), timeLimit, 1024*memLimit, uploadTime
                    )
                    userResult  = 'env/output.txt'
                    solution    = 'source/' + probName + '/' + str(x + 1) + '.sol'

                    if t == enum.ESC['TLE']:
                        result = 'TLE'
                        fileIO.write(
                            'env/error.txt', 'Time Limit Exceeded - Process killed.'
                        )
                    elif t == enum.ESC['SIGSEGV']:
                        fileIO.write(
                            'env/error.txt', 'SIGSEGV||Segmentation fault (core dumped)\n' + fileIO.read('env/error.txt')
                        )
                    elif t == enum.ESC['SIGFPE']:
                        fileIO.write(
                            'env/error.txt', 'SIGFPE||Floating point exception\n' + fileIO.read('env/error.txt')
                        )
                    elif t == enum.ESC['SIGABRT']:
                        fileIO.write(
                            'env/error.txt', 'SIGABRT||Aborted\n' + fileIO.read('env/error.txt')
                        )
                    elif t != enum.ESC['NOMAL']:
                        fileIO.write(
                            'env/error.txt', 'NZEC||return code : ' + str(t) + '\n' + fileIO.read('env/error.txt')
                        )

                    sumTime += elapsedTime

                    if(result == None and t == 0):
                        if(cmpFunc(userResult, solution)):
                            ans += 'P'
                            cnt += 1
                        else:
                            perfect = False
                            ans += '-' 
                    elif(result == 'TLE'):
                        ans += 'T'
                        perfect = False
                    else:
                        ans += 'X'
                        perfect = False
                    
                    sql = 'UPDATE Result SET result = %s WHERE idResult = %s'
                    val = ('Running in testcase #' + str(x+1), submission[0])
                    myCursor.execute(sql, val)
                    mydb.commit()

                if contestMode : 
                    ans += ']'
                
                lastTest = int(sub)myCursor
        try:
            errmsg = fileIO.read('env/error.txt')
        except:
            errmsg = 'Something wrong.'
        
        print('TIME : ' + str(sumTime))
        score = (cnt / int(testcase)) * 100

        sql = 'UPDATE Result SET result = %s, score = %s, timeuse = %s, status = 1, errmsg = %s WHERE idResult = %s'
        val = (ans, score, round(sumTime, 2), errmsg, submission[0])
        myCursor.execute(sql, val)
        mydb.commit()

    mydb.commit()
    time.sleep(1)
