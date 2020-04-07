import subprocess
import os
import signal

import config
import time
import enum

# Compile the subject
def compile(fileName, userID, language):
    # God-damned dangerous 777. Change it maybe?
    os.system('chmod 777 compiled/' + fileName)
    os.system('rm compiled/' + fileName)

    if(language not in config.lang):
        return 'L'
    print('Compiling subject\'s file ...')

    compileCMD  =   config.lang[language]['compile']
    compileCMD  =   compileCMD.replace('[subjectFileName]', fileName)
    compileCMD  =   compileCMD.replace('[userID]', userID)

    os.system(compileCMD)

    if not os.path.exists('compiled/' + fileName):
        print('\t--> Error: Failed to compile subject\'s file.')
        return 'Compilation error'

    print('\t--> Subject\'s file successfully compiled.')
    return None

  

# Execute the subject
def execute(language, userID, probName, probID, testcase, timeLimit, memLimit, uploadTime):
    exeName     =   probID + '_' + uploadTime
    inputFile   =   ' <source/' + probName + '/' + testcase + '.in 1>env/output.txt 2>env/error.txt'

    cmd  =  'ulimit -v ' + str(memLimit) + ';' + config.lang[language]['execute'] + '; exit;'
    cmd  =  cmd.replace('[binName]', exeName)
    cmd  =  cmd.replace('[inputFile]', inputFile)

    # Heck! This shit is serious man. Don't go 777.
    os.system('chmod 777 .')
    if(os.path.exists('env/error.txt')):
        os.system('chmod 777 env/error.txt')
    if(os.path.exists('env/output.txt')):
        os.system('chmod 777 env/output.txt')
    
    startTime = time.time()
    proc = subprocess.Popen([cmd], shell=True, preexec_fn=os.setsid)

    try:
        proc.communicate(timeout=timeLimit)
        t = proc.returncode
    except subprocess.TimeoutExpired:
        t = enum.ESC['TLE']

    elapsedTime = time.time() - startTime
    
    os.system('chmod 777 .')
    if(os.path.exists('/proc/' + str(proc.pid))):
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    return t, elapsedTime
