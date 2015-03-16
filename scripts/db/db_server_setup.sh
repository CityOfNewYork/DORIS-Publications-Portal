# Database Server Setup (Initial installations)
# ---------------------------------------------
# PLEASE NOTE:
# This script must be run as the root user on the system.
# This script must be run from within this directory (DORIS-Publications-Portal/artifacts/scripts/db)

# store current path (directory mentioned above) for later use
export CWD=$PWD

# Reset Path to Use Python 2.6.6
export PATH="/usr/lib64/qt-3.3/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/CA/AccessControl/bin:/opt/CA/AccessControl/lbin"

# Setup Passwords
source $CWD/prod.password_store.sh

#  Install Development Tools
yum -y groupinstall "Development tools"
yum -y install python-devel python-setuptools
easy_install virtualenv

echo -e "Django = $DB_DJANGO\nRoot = $DB_PASS\nIndex = $DB_NDX" > /var/lib/mysql/.db_pass

# Install Expect
yum -y install expect

# Install MySQL and Dependencies
yum -y install mysql mysql-server mysql-devel


# Setup MySQL Data Directories
mkdir -p /db/mysql_data
chown -R mysql:mysql /db/mysql_data
mv /etc/my.cnf /etc/my.cnf.orig
cp $CWD/../../conf/my.cnf /etc/my.cnf
rm -rf /var/lib/mysql/mysql.sock
touch /tmp/mysql.sock
ln -sf /tmp/mysql.sock /var/lib/mysql/mysql.sock 

# Start MySQL
service mysqld start

# Configure MySQL
expect -c '
spawn "mysql_secure_installation"

expect "(enter for none):" { send "\r" }
expect "Set root password?" { send "Y\r" }
expect "New password:" { send "$env(DB_PASS)\r" }
expect "Re-enter new password:" { send "$env(DB_PASS)\r" }
expect "Remove anonymous users?" { send "Y\r" }
expect "Disallow root login remotely?" { send "Y\r" }
expect "Remove test database and access to it?" { send "Y\r" }
expect "Reload privilege tables now?" { send "Y\r" }

interact
'

# Create mysql user
mysql -u root -p$DB_PASS -e "CREATE DATABASE publications; USE publications; CREATE USER 'index'@'localhost' IDENTIFIED BY '$DB_NDX';"

# Download and Install Java (Oracle JDK)
cd /opt/
tar xzf $CWD/../../packages/jdk-7u72-linux-x64.tar.gz
cd /opt/jdk1.7.0_72/
alternatives --install /usr/bin/java java /opt/jdk1.7.0_72/bin/java 2
alternatives --config java
# Press Enter Here

# Install Elasticsearch
rpm --import http://packages.elasticsearch.org/GPG-KEY-elasticsearch
touch /etc/yum.repos.d/elasticsearch.repo
echo "[elasticsearch-1.4]
name=Elasticsearch repository for 1.4.x packages
baseurl=http://packages.elasticsearch.org/elasticsearch/1.4/centos
gpgcheck=1
gpgkey=http://packages.elasticsearch.org/GPG-KEY-elasticsearch
enabled=1" >> /etc/yum.repos.d/elasticsearch.repo
yum -y install elasticsearch

# Copy Elasticsearch Configuration
mv /etc/elasticsearch/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml.orig
cp $CWD/../../conf/elasticsearch.yml /etc/elasticsearch/
mkdir /db/es_logs
mkdir /db/es_data
chown -R elasticsearch:elasticsearch /db/es_logs/ /db/es_data/

# Copy Password File
cp $CWD/../../conf/certs/user.pwd /etc/elasticsearch/

# Ensure Elasticsearch Works
service elasticsearch start
service elasticsearch stop

# Install elasticsearch head
/usr/share/elasticsearch/bin/plugin --install mobz/elasticsearch-head

# Setup Supervisor
# easy_install supervisor
# echo_supervisord_conf > /etc/supervisord.conf
# mv /etc/supervisord.conf /etc/supervisord.conf.orig
# cp $CWD/../../conf/supervisord.conf /etc/
# mkdir /etc/supervisord.d/
# cp $CWD/../../conf/supervisord /etc/rc.d/init.d/

# chmod +x /etc/rc.d/init.d/supervisord
# chkconfig --add supervisord
# chkconfig supervisord on
# service supervisord start -c /etc/supervisord.conf

# Setup Elasticsearch Supervisor App
# mkdir /usr/share/elasticsearch/logs/
# cp $CWD/../../conf/supervisor_elasticsearch.conf /etc/supervisord.d/supervisor_elasticsearch.conf
# supervisorctl reread
# supervisorctl update
# supervisorctl status

# Start Elasticsearch
service elasticsearch start

# Install Nginx
rpm -Uhv $CWD/../../packages/nginx-release-centos-6-0.el6.ngx.noarch.rpm
yum install -y nginx

# #Set up Nginx
mkdir -p /etc/nginx/sites-enabled
mkdir -p /etc/nginx/sites-available
mkdir -p /db/nginx_es_logs/
mkdir -p /db/nginx_logs/

# Backup original Nginx configuration
mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.orig

# Backup default Nginx sites
mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak
mv /etc/nginx/conf.d/example_ssl.conf /etc/nginx/conf.d/example_ssl.conf.bak

# Copy over Nginx configuration
cp $CWD/../../conf/db_nginx.conf /etc/nginx/nginx.conf

# Place site configuration for Nginx in sites-available
cp $CWD/../../conf/elasticsearch.conf /etc/nginx/sites-available

# Symlink the site configuration to sites-enabled
ln -s /etc/nginx/sites-available/elasticsearch.conf /etc/nginx/sites-enabled/elasticsearch.conf

# Setup SSL
cp -r $CWD/../../conf/certs/ /etc/nginx/

# Start Nginx
service nginx start

# Activate and Setup Virtual Environment
virtualenv /var/lib/mysql/virtualenvs/gpp_env
source /var/lib/mysql/virtualenvs/gpp_env/bin/activate
pip install mysql-python elasticsearch

# populate db
mysql -u root -p$DB_PASS -e "set global net_buffer_length=1000000; set global max_allowed_packet=100000000;"
mysql -u root -p$DB_PASS publications <$CWD/../../publications.sql

# create user with select permission
mysql -u root -p$DB_PASS -e "GRANT SELECT ON publications.document TO 'index'@'localhost';"

# Index DB
python $CWD/../../application/index_db.py

# Return to initial directory
cd $CWD


