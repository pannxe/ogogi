# TODO Add some stuff.

from colorama import Fore, Style
import os
import abb
import subprocess


def help():
    print("help\t\tDisplay help page.")
    print("exit\t\tExit command mode.")
    print("t [args]\tIssue [args] to system terminal.")
    print("reload [name]\t reload [name] module.")
    print("shutdown\tTerminate OGOGI.")


def run():
    print(abb.bold + Fore.YELLOW + "OGOGI-shell" + Style.RESET_ALL + "$ ", end="")
    s = input()
    cmd = s.split(" ")
    if cmd[0] == "exit":
        return abb.INCMD["EXIT"], []
    elif cmd[0] == "t":
        args = ""
        for e in cmd[1:]:
            args += e + " "
        subprocess.call(args, shell=True)
        return abb.INCMD["NONE"], []
    elif cmd[0] == "shutdown":
        return abb.INCMD["SHUTDOWN"], []
    elif cmd[0] == "help":
        help()
    elif cmd[0] == "reload":
        return abb.INCMD["RELOAD"], cmd[1:]
    else:
        return 0, []
