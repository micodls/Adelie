#!/usr/bin/env python

import os
import sys
import platform
import subprocess
import shlex

def execute(command, option=None, abort_on_error=True):
    log('Executing command: {}'.format(command), 'debug')
    command = shlex.split(command)
    if option == None:
        return_code = subprocess.call(command) if is_linux() else subprocess.call(command, shell=True)
    elif option == 'quiet':
        dev_null = open(os.devnull, 'w')
        return_code = subprocess.call(command, stdout=dev_null, stderr=dev_null)
    elif option == 'pipe':
        return_code = subprocess.call(command, shell=True)
    elif option == 'check':
        return_code = subprocess.check_output(command)
    else:
        log('{} is an invalid option'.format(option), 'error')
        sys.exit(1)

    if abort_on_error:
        raise RuntimeError('{} returned {}'.format(command, return_code))

    return return_code

def is_linux():
    return platform.system().lower() == "linux"

def log(message, severity='info'):
    message = '[{}]: {}'.format(severity.upper(), message)
    message_length = len(message)
    print '=' * message_length
    print message
    print '=' * message_length

def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0