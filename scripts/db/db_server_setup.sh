# Database Server Setup (Initial installations)
# ---------------------------------------------
# PLEASE NOTE: 
# This script must be run as the root user on the system.
# This script must be run from within this directory (DORIS-Publications-Portal/artifacts/scripts/db)

# proxy, useradd mysql, wget

# store current path (directory mentioned above) for later use
export CWD=$PWD

# Update the server
yum -y update

#  Install Development Tools
yum -y groupinstall "Development tools"
yum -y install python-devel python-setuptools
easy_install virtualenv

# Install Expect
yum -y install expect

# Install MySQL and Dependencies
yum -y install mysql mysql-server mysql-devel

# Start MySQL
service mysqld start

# Configure MySQL
expect -c '
spawn "mysql_secure_installation"

expect "(enter for none):" { send -- "\r" }
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
mysql -u root -p$DB_PASS -e "CREATE DATABASE publications; USE publications; CREATE USER 'index'@'localhost' IDENTIFIED BY '$DB_NDX'; CREATE USER 'update_na'@'localhost' IDENTIFIED BY '$DB_UNA'"

# Download and Install Java (Oracle JDK)
cd /opt/
wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/7u72-b14/jdk-7u72-linux-x64.tar.gz"
tar xzf jdk-7u72-linux-x64.tar.gz
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
cp $CWD/../../conf/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml

# Copy Password File
cp $CWD/../../conf/user.pwd /etc/elasticsearch/user.pwd

# Ensure Elasticsearch Works
service elasticsearch start
service elasticsearch stop

# Install elasticsearch head
/usr/share/elasticsearch/bin/plugin --install mobz/elasticsearch-head

# Start Elasticsearch
service elasticsearch start

# Install Nginx
rpm -Uhv $CWD/../../packages/nginx-release-centos-6-0.el6.ngx.noarch.rpm
yum install -y nginx

# Set up Nginx
mkdir -p /etc/nginx/sites-enabled
mkdir -p /etc/nginx/sites-available

# Backup original Nginx configuration
mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.orig

# Copy over Nginx configuration
cp $CWD/../../conf/db_nginx.conf /etc/nginx/nginx.conf

# Place site configuration for Nginx in sites-available
cp $CWD/../../conf/es_nginx.conf /etc/nginx/sites-available

# Symlink the site configuration to sites-enabled
ln -s /etc/nginx/sites-available/es_nginx.conf /etc/nginx/sites-enabled/es_nginx.conf

# Setup SSL for Elasticsearch and Nginx
mkdir -p /etc/nginx/certs
cd /etc/nginx/certs
openssl genrsa 2048 > es.key
openssl req -new -x509 -nodes -sha1 -days 3650 -key es.key > es.cert
openssl x509 -noout -fingerprint -text < es.cert > es.info
cat es.cert es.key > es.pem

# Start Nginx
service nginx start

# Activate and Setup Virtual Environment
virtualenv /home/mysql/virtualenvs/gpp_env
source /home/mysql/virtualenvs/gpp_env/bin/activate
pip install mysql-python elasticsearch

# Populate DB
mysql -u root -p$DB_PASS -e "set global net_buffer_length=1000000; set global max_allowed_packet=100000000;"
mysql -u root -p$DB_PASS publications <$CWD/../../sql/publications.sql

# Insert Stored Procedure for Update Num Access
mysql -u root -p$DB_PASS publications <$CWD/../../sql/update_num_access.sql

# create user with select permission
mysql -u root -p$DB_PASS -e "GRANT SELECT ON publications.document TO 'index'@'localhost';"
mysql -u root -p$DB_PASS -e "GRANT EXECUTE ON PROCEDURE publications.update_num_access TO 'update_na'@'XXX.XXX.XXX.XXX' IDENTIFIED BY '$DB_UNA'"

# Index DB
python $CWD/../../application/index_db.py

# Return to initial directory
cd $CWD
