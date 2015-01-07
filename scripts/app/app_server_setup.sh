# Application Server Setup (Initial installations)
# ---------------------------------------------
# PLEASE NOTE: 
# This script must be run as the root user on the system.
# This script must be run from within this directory (DORIS-Publications-Portal/artifacts/scripts/app)

# Store current path (directory mentioned above) for later use
export CWD=$PWD

# Update the Server
yum -y update

# Install Development Tools
yum -y groupinstall "Development tools"
yum -y install python-devel python-setuptools python-setuptools-devel
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel mysql-devel libxml2-devel libxslt-devel unixODBC-devel sqlite sqlite-devel
# Install Nginx
rpm -Uhv ../../packages/nginx-release-centos-6-0.el6.ngx.noarch.rpm
yum install -y nginx

# Setup Nginx
mkdir -p /etc/nginx/sites-enabled
mkdir -p /etc/nginx/sites-available
mkdir -p /var/www/gpp
mkdir -p /var/www/logs/nginx
mkdir -p /var/www/gpp/static
mkdir -p /var/www/gpp/media

cp ../../conf/uwsgi_params /var/www/gpp/uwsgi_params

mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.orig
cp ../../conf/nginx.conf /etc/nginx/nginx.conf

ln -s ../../conf/gpp_django_nginx.conf /etc/nginx/sites-available

ln -s /etc/nginx/sites-available/gpp_django_nginx.conf /etc/nginx/sites-enabled/gpp_django_nginx.conf

/etc/init.d/nginx restart

# Install Virtualenv and Pip
easy_install virtualenv 
easy_install pip

# Install uWSGI Globally
pip install uwsgi

# Setup Django GPP Virtualenv
mkdir -p /var/www/virtualenvs/gpp_venv
virtualenv /var/www/virtualenvs/gpp_venv
source /var/www/virtualenvs/gpp_venv/bin/activate
pip install -r ../../conf/requirements.txt

# Setup Application
cp -r ../../application/doris_gpp-2.0.0/* /var/www/gpp
cp ../../conf/gpp_uwsgi.ini /var/www/gpp
cd /var/www/gpp
python manage.py syncdb --noinput