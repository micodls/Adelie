#!/usr/bin/env python

import sys
import platform
import subprocess
import shlex

def execute(command, option=None, abort_on_error=True):
    command = shlex.split(command)
    if option == None:
        return_code = subprocess.call(command) if is_linux() else subprocess.call(command, shell=True)
    elif option == 'quiet':
        dev_null = open(os.devnull, 'w')
        return_code = subprocess.call(command, stdout=dev_null, stderr=dev_null)
    elif option == 'pipe':
        return_code = subprocess.call(command, shell=True)
    else:
        print '[ERROR]: {} is an invalid option'.format(option)
        sys.exit(1)

    error_message = '{} returned {}'.format(command, return_code)

    if return_code == 0:
        return

    if abort_on_error:
        RuntimeError(error_message)
    else:
       print '[WARNING]: {}'.format(error_message)

def is_linux():
    return platform.system().lower() == "linux"