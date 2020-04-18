import fileIO
import abb


def runtimeHandler(t):
    if t == abb.ESC["TLE"]:
        fileIO.write("env/error.txt", "Time Limit Exceeded")
        return "TLE"
    elif t == abb.ESC["SIGSEGV"]:
        fileIO.write(
            "env/error.txt",
            "SIGSEGV||Segmentation fault (core dumped)\n"
            + fileIO.read("env/error.txt"),
        )
        return "SIGSEGV"
    elif t == abb.ESC["SIGFPE"]:
        fileIO.write(
            "env/error.txt",
            "SIGFPE||Floating point exception\n" + fileIO.read("env/error.txt"),
        )
        return "SIGFPE"
    elif t == abb.ESC["SIGABRT"]:
        fileIO.write(
            "env/error.txt", "SIGABRT||Aborted\n" + fileIO.read("env/error.txt")
        )
        return "SIGABRT"
    elif t == abb.ESC["NOMAL"]:
        return None
    else:
        fileIO.write(
            "env/error.txt",
            "NZEC||return code : " + str(t) + "\n" + fileIO.read("env/error.txt"),
        )
        return "ELSE"
