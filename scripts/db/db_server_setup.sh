# Database Server Setup (Initial installations)
# ---------------------------------------------
# PLEASE NOTE: 
# This script must be run as the root user on the system.
# This script must be run from within this directory (DORIS-Publications-Portal/artifacts/scripts/db)


# INCLUDE ALL TAR PACKAGES ETC.???

# store current path (directory mentioned above) for later use
export CWD=$PWD

# Update the server
yum -y update

#  Install Development Tools
yum -y groupinstall "Development tools"
yum -y install python-devel
yum -y install python-setuptools
easy_install virtualenv

export DB_PASS=$(openssl rand -base64 32)
export DB_NDX=$(openssl rand -base64 32)
export DB_DJANGO=$(openssl rand -base64 32)

echo -e "Django = $DB_DJANGO\nRoot = $DB_PASS\nIndex = $DB_NDX" >> /vagrant/db_pass.txt

# Install Expect
yum -y install expect

# Install Packages from RHEL Repositories
yum -y install mysql mysql-server mysql-devel

# Start MySQL
# /etc/init.d/mysqld start
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
mysql -u root -p$DB_PASS -e "CREATE DATABASE publications; USE publications; CREATE USER 'index'@'localhost' IDENTIFIED BY '$DB_NDX';"

# Download and Install Java (Oracle JDK)
cd /opt/
wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/7u72-b14/jdk-7u72-linux-x64.tar.gz"
tar xzf jdk-7u72-linux-x64.tar.gz #maybe we should just include this so we dont
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

groupadd es_mysql
mkdir /usr/share/es_mysql
chown -R root.es_mysql /usr/share/es_mysql
usermod -a -G es_mysql mysql
usermod -a -G es_mysql elasticsearch
chmod 775 /usr/share/es_mysql
chmod 2775 /usr/share/es_mysql
mv /etc/elasticsearch/elasticsearch.yml /usr/share/es_mysql/elasticsearch.yml.bak
mv /etc/elasticsearch/logging.yml /usr/share/es_mysql/logging.yml
cp $CWD/../../conf/elasticsearch.yml /usr/share/es_mysql/elasticsearch.yml
rm -rf /etc/elasticsearch
ln -s /usr/share/es_mysql/ /etc/elasticsearch
mkdir /usr/share/es_mysql/es_data
mkdir /usr/share/es_mysql/es_logs
mkdir /usr/share/es_mysql/es_plugins
chmod -R 775 /usr/share/es_mysql

service elasticsearch start
service elasticsearch stop
/usr/share/elasticsearch/bin/plugin --install head --url file:///vagrant/packages/elasticsearch-head.zip

service elasticsearch restart

# Index DB
virtualenv /home/mysql/.virtualenvs/gpp_env
source /home/mysql/.virtualenvs/gpp_env/bin/activate
pip install mysql-python elasticsearch

mysql -u root -p$DB_PASS -e "set global net_buffer_length=1000000; set global max_allowed_packet=100000000;"
mysql -u root -p$DB_PASS publications <$CWD/../../application/publications.sql

mysql -u root -p$DB_PASS -e "GRANT SELECT ON publications.gpp_document TO 'index'@'localhost';"

python $CWD/../../application/index_db.py

cd $CWD