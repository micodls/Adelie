#!/usr/bin/env python

import os
import helpers
import requests
from clint.textui import progress

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Installer:
    def __init__(self):
        self.__download_file()
        for application in self.__get_list_to_be_install():
            self.__install(application)
        # self.__update()
        # self.__upgrade()
        # self.__clean()

        # generic - works
        # self.__install("vim")
        # self.__install("curl")
        # self.__install("git")

        # self.__install("python-pip")
        # self.__install("python-setuptools")

        # google chrome
        # helpers.execute("wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -")
        # helpers.execute("sudo sh -c \"echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list\"")
        # self.__update()
        # self.__install("google chrome")

        # sublime
        # helpers.execute("sudo add-apt-repository ppa:webupd8team/sublime-text-3")
        # self.__update()
        # self.__install("sublime")

        # vlc
        # self.__install("vlc")

        # skype - not working
        # helpers.execute("sudo add-apt-repository "deb http://archive.canonical.com/ $(lsb_release -sc) partner"")
        # self.__update()
        # self.__install("skype")

        # spotify - not working (needs to be updated for 15.04)
        # helpers.execute("sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D2C19886")
        # helpers.execute("sudo sh -c \"echo "deb http://repository.spotify.com stable non-free" > /etc/apt/sources.list.d/spotify.list\"")
        # self.__update()
        # self.__install("spotify")

    def __install(self, application):
        command = self.__get_command_name(application)
        installer = self.__get_installer_name(application)

        print command, installer
        #if command is None or installer is None:
        #    helpers.log("{} not [yet] supported".format(alias), "warning")
        #else:
        #    try:
        #        helpers.log("Checking if {} is not yet installed.".format(alias), "debug")
        #        helpers.execute("{} --help".format(command), "quiet")
        #    except OSError as e:
        #        if e.errno == os.errno.ENOENT:
        #            helpers.log("Installing {}.".format(alias), "info")
        #            # helpers.execute("sudo apt-get install {}".format(installer))
        #    else:
        #        helpers.log("{} already installed.".format(alias), "info")

    def __update(self):
        # helpers.execute("echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf > /dev/null", "pipe") # hack for update
        helpers.execute("sudo apt-get update --quiet")

    def __upgrade(self):
        helpers.execute("sudo apt-get upgrade")

    def __clean(self):
        helpers.execute("sudo apt-get autoremove")
        helpers.execute("sudo apt-get autoclean")

    def __remove(self, command):
        helpers.execute("sudo apt-get purge {}".format(command))
        self.__clean()

    def __get_installer_name(self, application):
        installer_name = {
            "beyond compare": "packages/bcomapre.deb",
            "curl": "curl",
            "dropbox": "packages/dropbox.deb",
            "dtrx": "dtrx",
            "gdebi": "gdebi",
            "git": "git",
            "gitk": "gitk",
            "google chrome": "google-chrome-stable",
            "meld": "meld",
            "nodejs": "nodejs",
            "npm": "npm",
            "nyancat": "nyancat",
            "pandoc": "pandoc",
            "pip": "python-pip",
            "skype": "skype",
            "spotify": "spotify-client",
            "sublime": "sublime-text-installer",
            "texlive": "texlive-latex-base texlive-fonts-recommended texlive-latex-extra",
            "viber": "packages/viber.deb",
            "vim": "vim",
            "vlc": "vlc browser-plugin-vlc",
            "wine": "wine",
            "xclip": "xclip"
        }.get(application, None)

        if installer_name is None:
            raise RuntimeError("{} isn't a supported installer name.".format(application))

        return installer_name

    def __get_command_name(self, application):
        command_name = {
            "beyond compare": "bcompare",
            "curl": "curl",
            "dropbox": "dropbox",
            "dtrx": "dtrx",
            "gdebi": "gdebi",
            "git": "git",
            "gitk": "gitk",
            "google chrome": "google-chrome",
            "meld": "meld",
            "nodejs": "nodejs",
            "npm": "npm",
            "nyancat": "nyancat",
            "pandoc": "pandoc",
            "pip": "pip",
            "skype": "skype",
            "spotify": "spotify",
            "sublime": "subl",
            "texlive": "latex",
            "viber": "/opt/viber/Viber",
            "vim": "vim",
            "vlc": "vlc",
            "wine": "wine",
            "xclip": "xclip"
        }.get(application, None)

        if command_name is None:
            raise RuntimeError("{} isn't a supported command name.".format(application))

        return command_name

    def __get_list_to_be_install(self):
        list = []
        with open(os.path.join(__location__, "list")) as file:
            for line in file:
                if not line.lstrip().startswith("#"):
                    list.append(line.rstrip());

        return filter(None, list)

    def __download_file(self):
        r = requests.get("http://www.scootersoftware.com/bcompare-4.1.3.20814_amd64.deb", stream=True)
        # print os.path.relpath("packages")
        with open("/packages/bcompare-4.1.3.20814_amd64.deb", 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()
