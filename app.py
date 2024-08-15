#!/usr/bin/env python3
import os
import sys
try:
    import pyfiglet
except ModuleNotFoundError:
    os.system('sudo apt install python3-pip')
    os.system('sudo pip install pyfiglet --break-system-packages')
    os.system(f'python3 {os.path.dirname(os.path.realpath(sys.argv[0]) )}/app.py')
    exit(0)


basedir = os.path.dirname(os.path.realpath(sys.argv[0]) )
os.chdir(f"{basedir}/source/app")
sys.path.append(f"{basedir}/source/app")

print(os.listdir('.'))

import main

if __name__=="__main__":
    main.curses.wrapper(main.main)