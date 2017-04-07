#!/usr/bin/env bash

# setup.sh
# --------
#
# Must be run from project root.
#
# Setup GPP development environment.

# add vagrant box if not added
readonly DEFAULT_BOXPATH="./rhel-6.8.virtualbox.box"
echo Verifying vagrant box \"rhel-6.8-5.1.18\" added...
vagrant box list | grep rhel-6.8-5.1.18 >/dev/null 2>&1 || {
    echo Box not found.
    read -p "path to box file ($DEFAULT_BOXPATH): " boxpath
    boxpath=${boxpath:-$DEFAULT_BOXPATH}
    if [ -f $boxpath ]; then
        vagrant box add rhel-6.8-5.1.18 $boxpath
    else
        echo $boxpath not found
        exit 1
    fi
}

# install vagrant plugins if not installed
echo Checking vagrant plugins...
plugins=`vagrant plugin list`
echo $plugins | grep vagrant-reload >/dev/null 2>&1 || vagrant plugin install vagrant-reload
echo $plugins | grep vagrant-vbguest >/dev/null 2>&1 || vagrant plugin install vagrant-vbguest
echo $plugins | grep vagrant-triggers >/dev/null 2>&1 || vagrant plugin install vagrant-triggers

# Copy Vagrantfile.example if Vagrantfile not found
if [ ! -f Vagrantfile ]; then
    echo Copying Vagrantfile.example to Vagrantfile
    cp Vagrantfile.example Vagrantfile
    read -n1 -p "Would you like to stop this script and make changes to ./Vagrantfile? [y/n] " stop
    case $stop in
        y|Y) echo; echo Exiting; exit 0 ;;
    esac
    echo
fi

# get RedHat credentials from env or stdin
if [ "$RH_USER" -a "$RH_PASS" ]; then
    username=$RH_USER
    password=$RH_PASS
else
    echo Enter your RedHat Developer Account credentials
    read -p "username: " username
    read -s -p "password: " password
    echo
fi

# vagrant up with RedHat credentials as environment variables
RH_USER=$username RH_PASS=$password vagrant up
