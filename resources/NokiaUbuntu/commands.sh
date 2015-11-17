# nodejs and npm - nokia specific
curl -sL https://deb.nodesource.com/setup | sudo bash -
sudo apt-get install nodejs
sudo apt-get install build-essential
sudo ln -s /usr/bin/nodejs /usr/local/bin/node

# nodejs and npm  - will download ubuntu package defaults
sudo apt-get install nodejs
sudo apt-get install npm

# nokia nodejs and npm (https://confluence.int.net.nokia.com/display/MEGAZONE/Node.js)
sudo ln -s /usr/bin/nodejs /usr/local/bin/node
sudo npm install -g npm@2.11.3
# Download proper nodejs
# Windows: http://esmz02.emea.nsn-net.net:8080/job/megazone-node-js-Windows-installation-image/lastSuccessfulBuild/artifact/node/Release/node-v0.xx.x-x86.msi
# Linux: http://esmz02.emea.nsn-net.net:8080/job/megazone-node-js-Linux-installation-image/lastSuccessfulBuild/artifact/node/node-v0.xx.x-linux-x64.tar.gz
sudo mv node-v0.xx.x-linux-x64.tar.gz /opt/
sudo ln -s /opt/node-v0.xx.x-linux-x64.tar.gz/bin/node /usr/local/bin/node

# npm warn unmet dependency when you npm install
rm -rf node_modules/
npm cache clean

# shutter - snipping tool for linux - optional
sudo add-apt-repository ppa:shutter/ppa
sudo apt-get update
sudo apt-get install shutter

# git
sudo apt-get install git
sudo apt-get install gitk
git config --global user.name "<FULL_NAME>"
git config --global user.email <NOKIA_EMAIL>
git config --global push.default simple # git version < 2.0

# spotify
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D2C19886
echo deb http://repository.spotify.com stable non-free | sudo tee /etc/apt/sources.list.d/spotify.list
sudo apt-get update
sudo apt-get install spotify-client

# Sublime Text 3
sudo add-apt-repository ppa:webupd8team/sublime-text-3
sudo apt-get update
sudo apt-get install sublime-text-installer

# Beyond Compare 4 - download from http://www.scootersoftware.com/download.php
sudo gdebi bcompare-4.1.1.20615_amd64.deb

# google chrome
# sudo sh -c \'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list\' # echo is run in sudo but >> is not
echo "deb http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee -a /etc/apt/sources.list.d/google.list
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo apt-get update
sudo apt-get install google-chrome-stable

# everpad - evernote linux client - MEH
sudo add-apt-repository ppa:nvbn-rm/ppa
sudo apt-get update
sudo apt-get install everpad

# wine
sudo add-apt-repository ppa:ubuntu-wine/ppa -y
sudo apt-get update
sudo apt-get install wine

# skype
sudo add-apt-repository "deb http://archive.canonical.com/ $(lsb_release -sc) partner"
sudo apt-get update
sudo apt-get install skype

# pandoc - converts markdown to pdf - requires latex
sudo apt-get install pandoc

# linux release
lsb_release -a

# kernel version
uname -r

# update from 14.04.2 to 14.04.3
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install linux-generic-lts-vivid # to install kernel version
reboot

# WoW
wine Wow.exe -opengl

# sublime addons
# package control
# prettify
# markdownEditing
# markdown preview
# pandoc