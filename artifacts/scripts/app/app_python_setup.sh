# Application Server Setup - Python and Virtualenv Installation
# This script sets up python and the required packages for the Government
# Publications Portal
# This script must be run as the root user

# Install Virtualenv
easy_install virtualenv

# Install Pip
easy_install pip

# Install uWSGI
pip install uwsgi

# Setup User Virtualenv
sudo -u apache
mkdir -p ~/.virtualenvs/gpp_venv
virtualenv ~/.virtualenv/gpp_venv
exit

# Install Requirements
source /home/apache/.virtualenvs/gpp_venv/bin/activate
pip install -r ../../conf/requirements.txt

