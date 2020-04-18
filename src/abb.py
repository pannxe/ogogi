from colorama import Style, Fore

ESC = {"TLE": 124, "SIGSEGV": 139, "SIGFPE": 136, "SIGABRT": 134, "NOMAL": 0}

INCMD = {"EXIT": 0, "SHUTDOWN": 1, "RELOAD": 2, "NONE": 3}

bold = "\033[1m"
error = "[ " + bold + Fore.RED + "Error" + Style.RESET_ALL + " ] "
ok = "[ " + bold + Fore.GREEN + "OK" + Style.RESET_ALL + " ] "
