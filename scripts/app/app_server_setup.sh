# Application Server Setup (Initial installations)
# ---------------------------------------------
# PLEASE NOTE:
# This script must be run as the root user on the system.
# This script must be run from within this directory (DORIS-Publications-Portal/artifacts/scripts/app)

# Store current path (directory mentioned above) for later use
export CWD=$PWD

# Reset Path to Use Python 2.6.6
export PATH="/usr/lib64/qt-3.3/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/CA/AccessControl/bin:/opt/CA/AccessControl/lbin"

# Install Development Tools
yum -y groupinstall "Development tools"
yum -y install python-devel python-setuptools python-setuptools-devel
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel mysql-devel libxml2-devel libxslt-devel unixODBC-devel sqlite sqlite-devel

# Install Nginx
rpm -Uhv $CWD/../../packages/nginx-release-centos-6-0.el6.ngx.noarch.rpm
yum install -y nginx

# Create folders for application
mkdir -p /var/www/gpp_root
mkdir -p /var/www/logs/nginx
mkdir -p /var/www/gpp_root/static
mkdir -p /var/www/gpp_root/media

#Set up Nginx
mkdir -p /etc/nginx/sites-enabled
mkdir -p /etc/nginx/sites-available

# Backup original Nginx configuration
mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.orig

# Backup default Nginx sites
mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak
mv /etc/nginx/conf.d/example_ssl.conf /etc/nginx/conf.d/example_ssl.conf.bak

# Copy over Nginx configuration
cp $CWD/../../conf/app_nginx.conf /etc/nginx/nginx.conf

# Place site configuration for Nginx in sites-available
cp $CWD/../../conf/gpp_nginx.conf /etc/nginx/sites-available

# Symlink the site configuration to sites-enabled
ln -s /etc/nginx/sites-available/gpp_nginx.conf /etc/nginx/sites-enabled/gpp_nginx.conf

# uWSGI Configuration
cp $CWD/../../conf/uwsgi_params /var/www/gpp_root/uwsgi_params

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
pip install -r $CWD/../../conf/requirements.txt

# Deploy Application
cd $CWD
source app_migration.sh

# Restart Application
sh /var/www/gpp_root/restart_gpp.sh
