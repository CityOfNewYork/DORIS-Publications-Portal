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
rpm -Uhv $CWD../../packages/nginx-release-centos-6-0.el6.ngx.noarch.rpm
yum install -y nginx

# Create folders for application
mkdir -p /var/www/gpp
mkdir -p /var/www/logs/nginx
mkdir -p /var/www/gpp/static
mkdir -p /var/www/gpp/media

# Setup Nginx
mkdir -p /etc/nginx/sites-enabled
mkdir -p /etc/nginx/sites-available

# Backup original Nginx configuration
mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.orig

# Copy over Nginx configuration
cp $CWD../../conf/nginx.conf /etc/nginx/nginx.conf

# Place site configuration for Nginx in sites-available
cp $CWD../../conf/gpp_nginx.conf /etc/nginx/sites-available

# Symlink the site configuration to sites-enabled
ln -s /etc/nginx/sites-available/gpp_nginx.conf /etc/nginx/sites-enabled/gpp_nginx.conf

# uWSGI Configuration
cp $CWD../../conf/uwsgi_params /var/www/gpp/uwsgi_params

# Restart Nginx
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
pip install -r $CWD../../conf/requirements.txt

# Setup Application
cp -r $CWD../../application/doris_gpp-2.0.0/* /var/www/gpp
cp $CWD../../conf/gpp_uwsgi.ini /var/www/gpp
cd /var/www/gpp
python manage.py syncdb --noinput