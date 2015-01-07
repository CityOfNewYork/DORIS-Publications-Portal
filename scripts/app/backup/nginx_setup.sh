# Application Server Setup - Apache Setup
# This script will setup nginx for the Government Publications Portal 
# Django Application
# Nginx will be used to server static files.
# The script must be run as the root user

# Create Sites-Enabled and Sites-Available
mkdir /etc/nginx/sites-enabled
mkdir /etc/nginx/sites-available

# Backup default nginx.conf
mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.orig

# Copy new default nginx.conf
cp ../../conf/nginx.conf /etc/nginx/

# Copy GPP Site to Nginx
cp ../../conf/gpp_django_nginx.conf /etc/nginx/sites-available/

# Create symlink for GPP Site
ln -s /etc/nginx/sites-available/gpp_django_nginx.conf etc/nginx/sites-enabled/gpp_django_nginx.conf

# Restart nginx
/etc/init.d/nginx restart