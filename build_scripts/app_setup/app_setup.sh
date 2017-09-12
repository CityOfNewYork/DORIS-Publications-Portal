#!/usr/bin/env bash

# 1. Install Python 2.7
yum -y install python27

# 2. Setup /etc/profile.d/python.sh
bash -c "printf '#\!/bin/bash\nsource /opt/rh/python27/enable\n' > /etc/profile.d/python27.sh"

# 3. Install MySQL Python connector
yum -y install python27-MySQL-python
# yum -y install python-devel mysql-devel

# yum -y install openssl-devel
# yum -y install libffi-devel

# 6. Install Required pip Packages
source /opt/rh/python27/enable
pip install virtualenv
mkdir /home/vagrant/.virtualenvs

virtualenv --system-site-packages /home/vagrant/.virtualenvs/gpp

# Is this needed?
# chown -R vagrant:vagrant /home/vagrant

# Install uwsgi globally
pip install uwsgi

source /home/vagrant/.virtualenvs/gpp/bin/activate
pip install -r /vagrant/conf/requirements.txt --no-binary :all:

# 7. Install telnet-server
yum -y install telnet-server

# 8. Install telnet
yum -y install telnet

# 9. Automatically Use Virtualenv
echo "source /home/vagrant/.virtualenvs/gpp/bin/activate" >> /home/vagrant/.bash_profile

# 9. Add the following lines to /etc/sudoers file
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis start
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis stop
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis status
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis restart
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis condrestart
#womens_activism   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis try-restart
