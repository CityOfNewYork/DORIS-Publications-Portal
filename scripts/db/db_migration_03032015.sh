# Deployment for Database Server - March 3rd, 2015
# Description:
# This script performs the following operations:
#	- Configures supervisord
#	- Configures elasticsearch for supervisor
#	- Moves elasticsearch index location and data
#   - Moves MySQL Data Directory
#	- Reconfigures some parts of nginx and elasticsearch
# PLEASE NOTE: The script should be run from the folder in which it is contained.

# Store Current Directory
export CWD=$PWD

# Setup Passwords
source ../db/prod.password_store.sh

# Stop Running Processes
sudo service elasticsearch stop
sudo service mysqld stop
sudo service nginx stop

# Reconfigure Nginx
sudo cp ../../conf/elasticsearch.conf /etc/nginx/sites-available
sudo cp ../../conf/db_nginx.conf /etc/nginx/nginx.conf

# Move MySQL
sudo mkdir /db/mysql_data
tar -cvf mysql.tar /var/lib/mysql
sudo mv /etc/my.cnf /etc/my.cnf.orig
sudo cp ../../conf/my.cnf /etc/my.cnf
sudo nohup rsync -avp /var/lib/mysql/ /db/mysql_data
sudo rsync -avp --delete /var/lib/mysql/ /db/mysql_data
sudo chown -R mysql:mysql /db/mysql_data
sudo rm -rf /tmp/mysql.sock
sudo ln -sf /db/mysql_data/mysql.sock /tmp/mysql.sock
sudo rm -rf /var/lib/mysql/*

# Move Elasticsearch Index to External Storage
sudo cp ../../conf/elasticsearch.yml /etc/elasticsearch/
sudo mv /var/lib/elasticsearch/doris_gpp /db/doris_gpp
mkdir /db/es_logs
sudo mv /var/log/elasticsearch/* /db/es_logs
sudo ln -s /etc/elasticsearch /usr/share/elasticsearch/config

# Install Supervisor
sudo easy_install supervisor

# Setup Supervisor
sudo echo_supervisord_conf > /etc/supervisord.conf
sudo mv /etc/supervisord.conf /etc/supervisord.conf.orig
sudo cp ../../conf/supervisord.conf /etc/
sudo mkdir /etc/supervisord.d/
sudo cp ../../conf/supervisord /etc/rc.d/init.d/

sudo chmod +x /etc/rc.d/init.d/supervisord
sudo chkconfig --add supervisord
sudo chkconfig supervisord on
sudo service supervisord start

# Setup Elasticsearch Supervisor App
sudo mkdir /usr/share/elasticsearch/logs
sudo cp ../../conf/supervisor_elasticsearch.conf /etc/supervisord.d/supervisor_elasticsearch.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status

# Start Processes Again
sudo supervisorctl start supervisor_elasticsearch
sudo service mysqld start
sudo service nginx start






