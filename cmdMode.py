# TODO Add some stuff.

import os

def run():
    while True:
        print('> ', end="")
        s = input()
        cmd = s.split(" ")
        if cmd[0] == 'exit':
            return None
        elif cmd[0] == 't':
            args = ''
            for e in cmd[1:]:
                args += e + ' '
            os.system(args)
        elif cmd[0] == 'shutdown':
            return 1
        else:
            return 0
