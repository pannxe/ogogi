IORedirect = ' 0<env/input.txt 1>env/output.txt 2>env/error.txt'
lang = {
    'C': {
        'extension' : 'c',
        'system'    : 'find /usr/bin/ -name gcc',
        'compile'   : 'gcc ../uploaded/[userID]/[subjectFileName].c -O2 -fomit-frame-pointer -o compiled/[subjectFileName]' + IORedirect,
        'execute'   : 'compiled/[binName][inputFile]'
    },
    'C++': {
        'extension' : 'cpp',
        'system'    : 'find /usr/bin/ -name g++',
        'compile'   : 'g++ ../uploaded/[userID]/[subjectFileName].cpp -O2 -fomit-frame-pointer -o compiled/[subjectFileName]'+ IORedirect,
        'execute'   : 'compiled/[binName][inputFile]'
    }
}