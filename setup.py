#!/usr/bin/env python

import time
import os
import sys
import subprocess
import shlex
import helpers

class Logger:
    def __init__(self):
        print ''

    def log(self, severity, message):
        print 'log'

class Installer:
    def __init__(self):
        print ''
        # self.__update()
        # self.__upgrade()
        # self.__clean()

        # generic - works
        # self.__install('vim')
        # self.__install('curl')
        # self.__install('git')

        # self.__install('python-pip')
        # self.__install('python-setuptools')

        # google chrome - works
        # helpers.execute('wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -')
        # helpers.execute('sudo sh -c \'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list\'')
        # self.__install('google chrome')

        # sublime - works
        # helpers.execute('sudo add-apt-repository ppa:webupd8team/sublime-text-3')
        # self.__install('sublime')

        # vlc - works
        # self.__install('vlc')

    def __install(self, alias):
        command = self.__get_command_name(alias)
        installer = self.__get_installer_name(alias)

        try:
            print '[INFO]: Checking if {} is not yet installed.'.format(alias)
            helpers.execute('{} --help'.format(command), 'quiet')
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                print '[INFO]: Installing {}.'.format(alias)
                helpers.execute('sudo apt-get install {}'.format(installer))

    def __update(self):
        # helpers.execute('echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf > /dev/null', 'pipe') # hack for update
        helpers.execute('sudo apt-get update')

    def __upgrade(self):
        helpers.execute('sudo apt-get upgrade')

    def __clean(self):
        helpers.execute('sudo apt-get autoremove')
        helpers.execute('sudo apt-get clean')

    def __remove(self, command):
        helpers.execute('sudo apt-get remove {}'.format(command))

    def __get_installer_name(self, alias):
        installer_name = {
            'vim': 'vim',
            'curl': 'curl',
            'git': 'git',
            'google chrome': 'google-chrome-stable',
            'vlc': 'vlc browser-plugin-vlc',
            'sublime': 'sublime-text-installer'
        }.get(alias, None)

        if installer_name == None:
            print '[WARNING]: {} not [yet] supported'.format(alias)

        return installer_name

    def __get_command_name(self, alias):
        command_name = {
            'vim': 'vim',
            'curl': 'curl',
            'git': 'git',
            'google chrome': 'google-chrome',
            'vlc': 'vlc',
            'sublime': 'subl'
        }.get(alias, None)

        if command_name == None:
            print '[WARNING]: {} not [yet] supported'.format(alias)

        return command_name

class BitBucket:
    def __init__(self):
        try:
            helpers.execute('pip show bitbucket-api')
        except ImportError as e:
            print e

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

class Timer:
    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, type, value, traceback):
        elapsed_time = time.time() - self.start_time
        minutes, seconds = divmod(elapsed_time, 60)
        print "Elapsed Time: %02dm %02ds" % (minutes, seconds)

def main():
    with Timer():
        Installer()
        # git = Git()
        # git.clone()

if __name__ == '__main__':
    main()

# skype
# viber
# spotfy

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

