# app_migration.sh
# ----------------

# suspend processes
service nginx stop
killall -s INT /usr/bin/uwsgi

# migrate
rm -rf /var/www/gpp/
cp -rf gpp /var/www/

# resume processes
service nginx restart
uwsgi --socket /var/www/gpp/mysite.sock --chmod-socket=666 --processes=10 --wsgi-file=/var/www/gpp/django_gpp/wsgi.py --daemonize=/var/www/logs/gpp_uwsgi.log --vacuum