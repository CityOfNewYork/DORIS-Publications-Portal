# Application Server Setup - Virtualenv Setup
# This script will setup the virtualenvironment for the Government Publications
# Portal Django Application
# The script must be run as the local user (admin)
CWD = "$PWD"

# Create virtual environment
mkdir $HOME/.virtualenvs/gpp_venv
vitrualenv $HOME/.virtualenvs/gpp_venv

# Activate the virtual environment
source $HOME/.virtualenvs/gpp_venv

# Install required packages
$HOME/python/Python-2.7.8/bin/pip install -r CWD/application/requirements.txt