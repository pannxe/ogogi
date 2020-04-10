import subprocess
import os
import signal

import config
import time
import abb
import fileIO

# Compile the subject
def compile(fileName, userID, language):
    if os.path.exists("compiled/" + fileName):
        os.system("chmod 777 compiled/" + fileName)
        os.system("rm compiled/" + fileName)

    if language not in config.lang:
        return "NOLANG"

    print("Compiling subject's file...")

    compileCMD = config.lang[language]["compile"]
    compileCMD = compileCMD.replace("[subjectFileName]", fileName)
    compileCMD = compileCMD.replace("[userID]", userID)

    os.system(compileCMD)

    if not os.path.exists("compiled/" + fileName):
        return "NOCMP"

    return None


# Execute the subject
def execute(
    language, userID, probName, probID, atCase, timeLimit, memLimit, uploadTime
):
    exeName = probID + "_" + uploadTime
    IORedirect = (
        "<source/" + probName + "/" + atCase + ".in 1>env/output.txt 2>env/error.txt"
    )
    cmd = (
        "ulimit -v "
        + str(memLimit)
        + ";"
        + config.lang[language]["execute"]
        + "; exit;"
    )
    cmd = cmd.replace("[binName]", exeName).replace("[IORedirect]", IORedirect)

    # Why do we have to chmod this?
    # os.system('chmod 777 .')
    if os.path.exists("env/error.txt"):
        os.system("chmod 777 env/error.txt")
    if os.path.exists("env/output.txt"):
        os.system("chmod 777 env/output.txt")

    startTime = time.time()
    proc = subprocess.Popen([cmd], shell=True, preexec_fn=os.setsid)

    try:
        proc.communicate(timeout=timeLimit)
        t = proc.returncode
    except subprocess.TimeoutExpired:
        t = abb.ESC["TLE"]

    elapsedTime = time.time() - startTime

    os.system("chmod 777 .")
    if os.path.exists("/proc/" + str(proc.pid)):
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    return t, elapsedTime
