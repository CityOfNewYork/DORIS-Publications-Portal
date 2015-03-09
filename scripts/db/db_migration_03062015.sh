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