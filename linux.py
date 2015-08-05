#!/usr/bin/env python

import helpers

class Installer:
    def __init__(self):
        print 'HERE'
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