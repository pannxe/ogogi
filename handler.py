import fileIO
import otogEnum


def runtimeHandler(t):
    if t == otogEnum.ESC["TLE"]:
        fileIO.write("env/error.txt", "Time Limit Exceeded - Process killed.")
        return "TLE"
    elif t == otogEnum.ESC["SIGSEGV"]:
        fileIO.write(
            "env/error.txt",
            "SIGSEGV||Segmentation fault (core dumped)\n"
            + fileIO.read("env/error.txt"),
        )
        return "SIGSEGV"
    elif t == otogEnum.ESC["SIGFPE"]:
        fileIO.write(
            "env/error.txt",
            "SIGFPE||Floating point exception\n" + fileIO.read("env/error.txt"),
        )
        return "SIGFPE"
    elif t == otogEnum.ESC["SIGABRT"]:
        fileIO.write(
            "env/error.txt", "SIGABRT||Aborted\n" + fileIO.read("env/error.txt")
        )
        return "SIGABRT"
    elif t != otogEnum.ESC["NOMAL"]:
        fileIO.write(
            "env/error.txt",
            "NZEC||return code : " + str(t) + "\n" + fileIO.read("env/error.txt"),
        )
        return "ELSE"
