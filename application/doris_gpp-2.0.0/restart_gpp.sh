cd /var/www/gpp_root/
export PATH=$PATH:/usr/local/bin
export ELASTICSEARCH=192.168.10.3
service rh-nginx18-nginx stop
killall uwsgi
source /home/vagrant/.virtualenvs/gpp/bin/activate
mkdir -p /var/www/logs/
/opt/rh/python27/root/usr/bin/uwsgi --socket /var/www/gpp_root/mysite.sock --chmod-socket=777 --processes=10 --wsgi-file=/var/www/gpp_root/django_gpp/wsgi.py --daemonize=/tmp/gpp_uwsgi.log --virtualenv=/home/vagrant/.virtualenvs/gpp --lazy-apps --touch-chain-reload --vacuum
service rh-nginx18-nginx start
