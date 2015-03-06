# Elasticsearch Setup
# Stop Running Processes
service elasticsearch stop
service mysqld stop
service nginx stop

# Move MySQL
mkdir /db/mysql_data
tar -cvf mysql.tar /var/lib/mysql
mv /etc/my.cnf /etc/my.cnf.orig
cp $CWD/../../conf/my.cnf /etc/my.cnf
nohup rsync -avp /var/lib/mysql/ /db/mysql_data
rsync -avp --delete /var/lib/mysql/ /db/mysql_data
chown -R mysql:mysql /db/mysql_data
rm -rf /tmp/mysql.sock
ln -sf /db/mysql_data/mysql.sock /tmp/mysql.sock
rm -rf /var/lib/mysql/*

# Move Elasticsearch Index to External Storage
cp $CWD/../../conf/elasticsearch.yml /etc/elasticsearch/
mv /var/lib/elasticsearch/doris_gpp /db/doris_gpp
mkdir /db/es_logs
mv /var/log/elasticsearch/* /db/es_logs
ln -s /etc/elasticsearch /usr/share/elasticsearch/config

# Install Supervisor
easy_install supervisor

# Setup Supervisor
echo_supervisord_conf > /etc/supervisord.conf
mv /etc/supervisord.conf /etc/supervisord.conf.orig
cp $CWD/../../conf/supervisord.conf /etc/
mkdir /etc/supervisord.d/
cp $CWD/../../conf/supervisord /etc/rc.d/init.d/

chmod +x /etc/rc.d/init.d/supervisord
chkconfig --add supervisord
chkconfig supervisord on
service supervisord start

# Setup Elasticsearch Supervisor App
mkdir /usr/share/elasticsearch/logs
cp $CWD/../../conf/supervisor_elasticsearch.conf /etc/supervisord.d/supervisor_elasticsearch.conf
supervisorctl reread
supervisorctl update
supervisorctl status

# Start Processes Again
supervisorctl start supervisor_elasticsearch
service mysqld start
service nginx start