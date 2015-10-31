#!/usr/bin/env python

import os
import helpers

class Installer:
    def __init__(self):
        self.__update()
        self.__upgrade()
        self.__clean()

        # generic - works
        self.__install('vim')
        self.__install('curl')
        self.__install('git')

        # self.__install('python-pip')
        # self.__install('python-setuptools')

        # google chrome
        # helpers.execute('wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -')
        # helpers.execute('sudo sh -c \'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list\'')
        # self.__update()
        self.__install('google chrome')

        # sublime
        # helpers.execute('sudo add-apt-repository ppa:webupd8team/sublime-text-3')
        # self.__update()
        self.__install('sublime')

        # vlc
        self.__install('vlc')

        # skype - not working
        # helpers.execute('sudo add-apt-repository "deb http://archive.canonical.com/ $(lsb_release -sc) partner"')
        # self.__update()
        self.__install('skype')

        # spotify - not working (needs to be updated for 15.04)
        # helpers.execute('sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D2C19886')
        # helpers.execute('sudo sh -c \'echo "deb http://repository.spotify.com stable non-free" > /etc/apt/sources.list.d/spotify.list\'')
        # self.__update()
        self.__install('spotify')

    def __install(self, alias):
        command = self.__get_command_name(alias)
        installer = self.__get_installer_name(alias)

        if command is None or installer is None:
            helpers.log('{} not [yet] supported'.format(alias), 'warning')
        else:
            try:
                helpers.log('Checking if {} is not yet installed.'.format(alias), 'debug')
                helpers.execute('{} --help'.format(command), 'quiet')
            except OSError as e:
                if e.errno == os.errno.ENOENT:
                    helpers.log('Installing {}.'.format(alias), 'info')
                    helpers.execute('sudo apt-get install {}'.format(installer))
            else:
                helpers.log('{} already installed.'.format(alias), 'info')

    def __update(self):
        # helpers.execute('echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf > /dev/null', 'pipe') # hack for update
        helpers.execute('sudo apt-get update')

    def __upgrade(self):
        helpers.execute('sudo apt-get upgrade')

    def __clean(self):
        helpers.execute('sudo apt-get autoremove')
        helpers.execute('sudo apt-get autoclean')

    def __remove(self, command):
        helpers.execute('sudo apt-get purge {}'.format(command))
        self.__clean()

    def __get_installer_name(self, alias):
        installer_name = {
            'vim': 'vim',
            'curl': 'curl',
            'git': 'git',
            'google chrome': 'google-chrome-stable',
            'vlc': 'vlc browser-plugin-vlc',
            'sublime': 'sublime-text-installer',
            'skype': 'skype',
            'spotify': 'spotify-client'
        }.get(alias, None)

        return installer_name

    def __get_command_name(self, alias):
        command_name = {
            'vim': 'vim',
            'curl': 'curl',
            'git': 'git',
            'google chrome': 'google-chrome',
            'vlc': 'vlc',
            'sublime': 'subl',
            'skype': 'skype',
            'spotify': 'spotify'
        }.get(alias, None)

        return command_name