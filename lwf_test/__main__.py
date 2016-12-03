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
HERE = path.abspath(path.dirname(__file__))

def argHandle(args):
    ret = True
    if('-i' in args):
        print(lwf_test.__doc__)
    elif('-h' in args):
        help(lwf_test)
    elif('-t' in args):
        package_tests.run()
        ret = False
    return ret
    
def main(args = None):
    
    if(argHandle(args or sys.argv)):
        print(path.join(HERE, CONSOLE_HELP_FILE))
        with open(path.join(HERE, CONSOLE_HELP_FILE), encoding='utf-8') as f:
            print(f.read())
            
if __name__ == "__main__":
    main()