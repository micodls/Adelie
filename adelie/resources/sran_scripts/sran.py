#!/usr/bin/env python

# Basic SRAN scripts
# Author: Paolo Miguel M. de los Santos
# Email: paolo.de_los_santos@nokia.com

import time
import subprocess
import sys
import shlex
import argparse

class ArgsParser:
    def __init__(self):
        class CustomFormatter(argparse.RawTextHelpFormatter, argparse.RawDescriptionHelpFormatter) :
            pass

        parser = argparse.ArgumentParser(prog = 'sran',
            usage = '%(prog)s <subcommand> [options][args]',
            formatter_class = CustomFormatter,
            add_help = False)

        subparser = parser.add_subparsers()

        # config
        config_parser = subparser.add_parser('config', conflict_handler = 'resolve')
        config_parser.add_argument('-cmd', default = 'config', help = argparse.SUPPRESS)

        # clone
        clone_parser = subparser.add_parser('clone', conflict_handler = 'resolve')
        clone_parser.add_argument('-cmd', default = 'clone', help = argparse.SUPPRESS)
        clone_parser.add_argument('source', nargs='?', help = 'source URL')
        clone_parser.add_argument('dest', nargs='?', help = 'dest URL')

        args = parser.parse_args()

        if args.cmd == 'config':
            GitConfigurator()
        elif args.cmd == 'clone' :
            if args.source == None :
                print 'ERROR: Empty source path! Try sran clone [source] [dest]'
            else :
                _clone(args)

class GitConfigurator:
    def __init__(self):
        self.set_user_info('email')
        self.set_user_info('name')
        self.set_default_configurations()
        # self.set_SSH()

    def set_user_info(self, value):
        try:
            _execute('git config --global user.%s' % (value), False)
        except subprocess.CalledProcessError:
            user_info = raw_input('Enter your %s: ' % (value))
            _execute('git config --global user.%s "%s"' % (value, user_info))

    def get_user_info(self, value):
        try:
            print value + ': ' + _execute('git config --global user.%s' % (value), False)
        except subprocess.CalledProcessError, e:
            self.set_user_info(value)

    def unset_user_info(self, value):
        _execute('git config --global --unset-all user.%s' % value)

    def set_default_configurations(self):
        _execute('git config --global core.autocrlf true')

    def set_SSH(self):
        _execute('ssh-keygen')

def _execute(command, strict=True):
    exit_code = subprocess.call(shlex.split(command)) if strict else subprocess.check_output(shlex.split(command))
    error_message = '"%s" exited with %s.' % (command, exit_code)

    if exit_code == 0:
        return

    if exit_code:
        return exit_code

    if strict:
        raise RuntimeError(error_message)

def _clone(args, SSH=False):
    _execute('git clone %s %s' % (_get_branch_link(args.source), args.dest if args.dest else ''))

def _get_branch_link(branch_name, SSH=False):
    if SSH:
        ssh_branch = {
            'nodeoam': 'git@esmz01.emea.nsn-net.net:megazone/nodeoam.git'
        }.get(branch_name, None)

        if ssh_branch is None:
            raise RuntimeError("%s isn't an alias of a maintenance branch." % (branch_name))

        return ssh_branch
    else:
        http_branch = {
            'nodeoam': 'http://esmz01.emea.nsn-net.net/megazone/nodeoam.git'
        }.get(branch_name, None)

        if http_branch is None:
            raise RuntimeError("%s isn't an alias of a maintenance branch." % (branch_name))

        return http_branch

class Timer:
    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, type, value, traceback):
        min, sec = divmod((time.time() - self.start_time), 60)
        print 'Elapsed time: %dm %ds' % (min, sec)

def main() :
    with Timer() :
        ArgsParser()

if __name__ ==  '__main__':
    main()