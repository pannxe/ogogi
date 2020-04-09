IORedirect = " 0<env/input.txt 1>env/output.txt 2>env/error.txt"
lang = {
    "C": {
        "extension": "c",
        "system": "find /usr/bin/ -name gcc",
        "compile": "gcc ../uploaded/[userID]/[subjectFileName].c -O2 -fomit-frame-pointer -o compiled/[subjectFileName]"
        + IORedirect,
        "execute": "compiled/[binName][inputFile]",
    },
    "C++": {
        "extension": "cpp",
        "system": "find /usr/bin/ -name g++",
        "compile": "g++ ../uploaded/[userID]/[subjectFileName].cpp -O2 -fomit-frame-pointer -o compiled/[subjectFileName]"
        + IORedirect,
        "execute": "compiled/[binName][inputFile]",
    },
    # Test adding new language via config.lang
    "Golang": {
        "extension": "go",
        "system": "find /usr/bin/ -name go",
        "compile": "go tool compile -o compiled/[subjectFileName] ../uploaded/[userID]/[subjectFileName].go"
        + IORedirect,
        "execute": "compiled/[binName][inputFile]",
    },
}

legacyScriptPath = "source/[probName]/script.php"
configPath = "source/[probName]/config.cfg"
subjectFileName = "[probID]_[uploadTime]"

resultPath = "env/output.txt"
solutionPath = "source/[probName]/[#].sol"

caseKey = "cases = "
caseKeyEnd = ";"

scriptPath = "source/[probName]/script.php"

interactivePath = "source/[probName]/interactive_script.php"

gradingInterval = 1
