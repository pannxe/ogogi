# TODO Add some stuff.

from colorama import Fore, Style
import os
import abb
import subprocess


def help():
    print("help\t\tDisplay help page.")
    print("exit\t\tExit command mode.")
    print("t [args]\tIssue [args] to system terminal.")
    print("shutdown\tTerminate OGOGI.")


def run():
    while True:
        print(abb.bold + Fore.YELLOW + "OGOGI-shell " + Style.RESET_ALL + "$ ", end="")
        s = input()
        cmd = s.split(" ")
        if cmd[0] == "exit":
            return None
        elif cmd[0] == "t":
            args = ""
            for e in cmd[1:]:
                args += e + " "
            subprocess.call(args, shell=True)
        elif cmd[0] == "shutdown":
            return 1
        elif cmd[0] == "help":
            help()
        else:
            return 0
