#!/usr/bin/env python

import os
import re
import helpers
import requests
from clint.textui import progress

class Installer:
    def __init__(self):
        self.__download_packages()
        for application in self.__get_list_to_be_install():
            self.__install(application)

    def __install(self, application):
        command = self.__get_command_name(application)
        installer = self.__get_installer_name(application)

        # print command, installer
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
            "beyond compare": "adelie/packages/bcompare-4.1.3.20814_amd64.deb",
            "curl": "curl",
            "dropbox": "adelie/packages/dropbox_2015.10.28_amd64.deb",
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
            "viber": "adelie/packages/viber.deb",
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
        with open("adelie/list") as file:
            for line in file:
                if not line.lstrip().startswith("#"):
                    list.append(line.rstrip());

        return filter(None, list)

    def __get_deb_links(self):
        list = []
        pattern = re.compile("http.*\.deb")
        with open("adelie/list") as file:
            for line in file:
                list += pattern.findall(line)

        return list

    def __download_packages(self):
        for deb_link in self.__get_deb_links():
            file_name =  deb_link.split("/")[-1]
            file_path = "adelie/packages/" + file_name
            if not os.path.isfile(file_path):
                helpers.log("Downloading {}".format(file_name), "info")
                self.__download_file(deb_link, file_path)
                helpers.log("Finished downloading {}".format(file_name), "info")
            else:
                helpers.log("{} already exists in packages".format(file_name), "debug")

    def __download_file(self, source, destination):
        request = requests.get(source, stream=True)
        with open(destination, 'wb') as file:
            total_length = int(request.headers.get('content-length'))
            for chunk in progress.bar(request.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                if chunk:
                    file.write(chunk)
                    file.flush()
