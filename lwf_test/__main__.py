# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 21:58:19 2016

@author: Tom Blanchet
"""
import sys
import lwf_test
from lwf_test import package_tests

from codecs import open
from os import path

CONSOLE_HELP_FILE = "console_help.txt"
README_FILE = "../README.txt"
HERE = path.abspath(path.dirname(__file__))

def argHandle(args):
    
    ret = True
    if('-i' in args):
        print(lwf_test.__doc__)
        ret = False
    elif('-h' in args):
        help(lwf_test)
        ret = False
    elif('-t' in args):
        package_tests.run()
        ret = False
    elif('-r' in args):
        global README_FILE
        printFile(README_FILE)
    return ret
    
def printFile(file):
    with open(path.join(HERE, file), encoding='utf-8') as f:
            print(f.read())
            
def main(args = None):
    
    if(argHandle(args or sys.argv)):
        print(path.join(HERE, CONSOLE_HELP_FILE))
        printFile(CONSOLE_HELP_FILE)
            
if __name__ == "__main__":
    main()