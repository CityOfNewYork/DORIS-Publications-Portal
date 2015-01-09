source /var/www/virtualenvs/gpp_venv/bin/activate
uwsgi --socket /var/www/gpp/mysite.sock --chmod-socket=666 --processes=10 --wsgi-file=/var/www/gpp/django_gpp/wsgi.py --daemonize=/var/www/logs/gpp_uwsgi.log --virtualenv=/var/www/virtualenvs/gpp_venv --vacuum
