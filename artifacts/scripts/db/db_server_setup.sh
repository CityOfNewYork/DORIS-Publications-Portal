# Database Server Setup
# PLEASE NOTE: This script must be run as the root user on the system.

# Update the server
yum -y update

# Install Packages from RHEL Repositories
yum -y install mysql mysql-server mysql-devel

# Start MySQL
/etc/init.d/mysqld start

# Download and Install Oracle JDK
wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" -P ../../install/ http://download.oracle.com/otn-pub/java/jdk/7u60-b19/jdk-7u60-linux-i586.rpm
rpm -Uvh ../../install/jdk-7u60-linux-i586.rpm

# Install ElasticSearch
rpm --import http://packages.elasticsearch.org/GPG-KEY-elasticsearch

touch /etc/yum.repos.d/elasticsearch.repo
echo "[elasticsearch-1.4]
name=Elasticsearch repository for 1.4.x packages
baseurl=http://packages.elasticsearch.org/elasticsearch/1.4/centos
gpgcheck=1
gpgkey=http://packages.elasticsearch.org/GPG-KEY-elasticsearch
enabled=1" >> /etc/yum.repos.d/elasticsearch.repo
yum -y install elasticsearch

# Setup Repos for Nginx
rpm -ivh ../../install/nginx-release-centos-6-0.el6.ngx.noarch.rpm

# Install Apache
yum install -y httpd

# Install Nginx
yum -y install nginx

# Create Sites-Enabled and Sites-Available
mkdir /etc/nginx/sites-enabled
mkdir /etc/nginx/sites-available

# Backup default nginx.conf
mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.orig

# Copy new default nginx.conf
cp ../../conf/nginx.conf /etc/nginx/

# Copy GPP Site to Nginx
cp ../../conf/es_nginx.conf /etc/nginx/sites-available/

# Create symlink for GPP Site
ln -s /etc/nginx/sites-available/es_nginx.conf etc/nginx/sites-enabled/es_nginx.conf

# Install Expect
yum -y install expect

# Restart nginx
/etc/init.d/nginx restart