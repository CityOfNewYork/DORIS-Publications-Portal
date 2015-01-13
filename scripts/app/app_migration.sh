# Application Server Migration (Release)
# ---------------------------------------------
# PLEASE NOTE: 
# This script must be run as the root user on the system.
# This script must be run from within this directory (artifacts/scripts/app)

# Store current path (directory mentioned above) for later use
export CWD=$PWD

# Suspend Process
service nginx stop
killall -s INT /usr/bin/uwsgi

# Setup Application
cp -r $CWD/../../application/doris_gpp-2.0.0/* /var/www/gpp
cd /var/www/gpp
python manage.py syncdb --noinput

# Resume Processes
service nginx restart
sh /var/www/gpp_root/restart_gpp.sh