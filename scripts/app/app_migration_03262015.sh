# Application Server Migration (Release)
# ---------------------------------------------
# PLEASE NOTE: 
# This script must be run as the root user on the system.
# This script must be run from within this directory (artifacts/scripts/app)

# Store current path (directory mentioned above) for later use
export CWD=$PWD

cd /var/www/gpp_root/
export PATH=$PATH:/usr/local/bin
export ELASTICSEARCH=10.155.122.166
sudo /etc/init.d/nginx stop
killall uwsgi
source /var/www/virtualenvs/gpp_venv/bin/activate

# Copy Migration Specific Files - Make sure to replace existing files
cp -r /var/www/artifacts/application/doris_gpp-2.0.0/template/* /var/www/gpp_root/template
cp -r /var/www/artifacts/application/doris_gpp-2.0.0/static/* /var/www/gpp_root/static
cp -r /var/www/artifacts/application/doris_gpp-2.0.0/gpp/* /var/www/gpp_root/gpp

/var/www/uwsgi-2.0.9/uwsgi --socket /var/www/gpp_root/mysite.sock --chmod-socket=777 --processes=10 --wsgi-file=/var/www/gpp_root/django_gpp/wsgi.py --daemonize=/var/www/logs/gpp_uwsgi.log --virtualenv=/var/www/virtualenvs/gpp_venv --lazy-apps --touch-chain-reload --vacuum
sudo /etc/init.d/nginx start
