# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 16:23:56 2021

@author: lbrin
"""

from strategies import Context
from shell import Shell, ManualControl


def main():
    """ """
    shell = Shell(ManualControl(), Context())
    shell.run_shell()
    
    return 0


if __name__ == '__main__':
    main()
