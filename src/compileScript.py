import os
import config

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
