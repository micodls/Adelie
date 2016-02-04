#!/usr/bin/env python

import time
import os
import sys
import subprocess
from adelie import helpers
from adelie import linux

# class BitBucket:
#     def __init__(self):
#         try:
#             # helpers.execute('pip show bitbucket-api')
#         except ImportError as e:
#             print e

# Fix this one
class Git:
    def __init__(self):
        print ''
        # self.__config()
        # self.__generate_SSH()

    def __config(self):
        helpers.execute('git config --global user.name "Mico de los Santos"')
        helpers.execute('git config --global user.email mico.dlsantos@gmail.com')

    def __generate_SSH(self):
        helpers.execute('ssh-keygen')

    def clone(self, source, dest, SSH=True):
        helpers.execute('git clone {} {}'.format(source, dest if dest else ''))

class GitConfigurator:
    def __init__(self):
        self.__set_user_info('email')
        # self.__set_user_info('name')
        # self.set_default_configurations()
        # self.set_SSH()

    def __set_user_info(self, value):
        try:
            helpers.execute('git config --global user.{}'.format(value), 'check')
        except subprocess.CalledProcessError:
            user_info = raw_input('Enter your {}: '.format(value))
            helpers._execute('git config --global user.{} "{}"'.format(value, user_info))

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

class Timer:
    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, type, value, traceback):
        elapsed_time = time.time() - self.start_time
        minutes, seconds = divmod(elapsed_time, 60)
        print "Elapsed Time: %02dm %02ds" % (minutes, seconds)

def main():
    with Timer():
        linux.Installer()
        # GitConfigurator()
        # git.clone()

if __name__ == '__main__':
    main()

# http://tecadmin.net/install-laravel-framework-on-ubuntu/
# https://bitbucket-api.readthedocs.org/en/latest/usage.html
# https://pypi.python.org/pypi/bitbucket-api/0.5.0
# https://getcomposer.org/doc/03-cli.md#install
# https://confluence.atlassian.com/display/BITBUCKET/Set+up+SSH+for+Git
# https://help.github.com/articles/generating-ssh-keys/
# http://askubuntu.com/questions/527551/how-to-access-a-git-repository-using-ssh
# http://tipsonubuntu.com/2015/03/24/install-skype-4-3-in-ubuntu-15-04/
# http://askubuntu.com/questions/293693/how-to-install-skype-with-ubuntu-13-04
# http://askubuntu.com/questions/91543/apt-get-update-fails-to-fetch-files-temporary-failure-resolving-error

