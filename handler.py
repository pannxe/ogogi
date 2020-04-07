import fileIO
import enum

def runtimeHandler(t):
    if t == enum.ESC['TLE']:
        fileIO.write('env/error.txt', 'Time Limit Exceeded - Process killed.')
        return 'TLE'
    elif t == enum.ESC['SIGSEGV']:
        fileIO.write('env/error.txt', 'SIGSEGV||Segmentation fault (core dumped)\n' + fileIO.read('env/error.txt'))
        return 'SIGSEGV'
    elif t == enum.ESC['SIGFPE']:
        fileIO.write('env/error.txt', 'SIGFPE||Floating point exception\n' + fileIO.read('env/error.txt'))
        return 'SIGFPE'
    elif t == enum.ESC['SIGABRT']:
        fileIO.write('env/error.txt', 'SIGABRT||Aborted\n' + fileIO.read('env/error.txt'))
        return 'SIGABRT'
    elif t != enum.ESC['NOMAL']:
        fileIO.write('env/error.txt', 'NZEC||return code : ' + str(t) + '\n' + fileIO.read('env/error.txt'))
        return 'ELSE'
