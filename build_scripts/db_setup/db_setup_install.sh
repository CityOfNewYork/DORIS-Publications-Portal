#!/usr/bin/env bash

# 1. Install MySQL and Dependencies
yum -y install mysql-server mysql mysql-devel

# bash -c "printf '#\!/bin/bash\nsource /opt/rh/mysql55/enable\n' > /etc/profile.d/mysql55.sh"

# 2. Setup data directory for MySQL (store data from MySQL where it's not normally stored)
mkdir -p /data/mysql
chown -R mysql:mysql /data/mysql

mv /etc/my.cnf /etc/my.cnf.orig
cp /vagrant/conf/my.cnf /etc/

# 3. Start mysql
service mysqld start

# Create symlink. Starting mysql creates .sock in the directory specified in my.cnf (socket parameter)
ln -sf /tmp/mysql.sock /var/lib/mysql/mysql.sock

# Create database 'publications' and mysql user (without password for DEV)
mysql -u root -e "CREATE DATABASE publications; USE publications; CREATE USER 'index'@'localhost';"

# Command for creating user with password
# mysql -u root -e "CREATE DATABASE publications; USE publications; CREATE USER 'index'@'localhost' IDENTIFIED BY 'Index';"
