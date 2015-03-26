cd /var/www/gpp_root/
export PATH=$PATH:/usr/local/bin
export ELASTICSEARCH=192.168.10.3
sudo /etc/init.d/nginx stop
killall uwsgi
source /var/www/virtualenvs/gpp_venv/bin/activate
uwsgi --socket /var/www/gpp_root/mysite.sock --chmod-socket=777 --processes=10 --wsgi-file=/var/www/gpp_root/django_gpp/wsgi.py --daemonize=/var/www/logs/gpp_uwsgi.log --virtualenv=/var/www/virtualenvs/gpp_venv --lazy-apps --touch-chain-reload --vacuum
sudo /etc/init.d/nginx start
