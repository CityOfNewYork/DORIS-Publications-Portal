# Application Server Migration (Release)
# ---------------------------------------------
# PLEASE NOTE: 
# This script must be run as the root user on the system.
# This script must be run from within this directory (artifacts/scripts/app)

# Store current path (directory mentioned above) for later use
export CWD=$PWD

# Activate virtualenv
source /home/vagrant/.virtualenvs/gpp/bin/activate

# Suspend Process
service rh-nginx18-nginx stop
killall -s INT /usr/bin/uwsgi

# Setup Application
rm -rf /var/www/gpp_root/*
cp -r /vagrant/application/doris_gpp-2.0.0/* /var/www/gpp_root
cd /var/www/gpp_root
python manage.py syncdb --noinput

# Resume Processes
service rh-nginx18-nginx restart
sh /var/www/gpp_root/restart_gpp.sh