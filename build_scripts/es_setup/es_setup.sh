#!/usr/bin/env bash
# 1. Install Java
yum -y install java-1.8.0-openjdk

wget https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.4.5.noarch.rpm -P /tmp

# 2. Install ElasticSearch
rpm -ivh /tmp/elasticsearch-1.4.5.noarch.rpm

# 3. Autostart ElasticSearch
/sbin/chkconfig --add elasticsearch
chkconfig elasticsearch on

# 4. Configure ElasticSearch
mv /etc/elasticsearch/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml.orig
ln -s /vagrant/conf/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml

# Install nginx and create ssl certs if not running on a single server
if [ "$1" != single_server ]; then
    echo "complete complete complete COMPLETE"
    yum -y install rh-nginx18-nginx

    bash -c "printf '#\!/bin/bash\nsource /opt/rh/rh-nginx18/enable'"

    mv /etc/opt/rh/rh-nginx18/nginx/nginx.conf /etc/opt/rh/rh-nginx18/nginx/nginx.conf.orig

    ln -s /vagrant/build_scripts/es_setup/nginx_conf/nginx.conf /etc/opt/rh/rh-nginx18/nginx/nginx.conf

    openssl req \
           -newkey rsa:4096 -nodes -keyout /vagrant/build_scripts/es_setup/elasticsearch_dev.key \
           -x509 -days 365 -out /vagrant/build_scripts/es_setup/elasticsearch_dev.crt -subj "/C=US/ST=New York/L=New York/O=NYC Department of Records and Information Services/OU=IT/CN=womensactivism.nyc"
    openssl x509 -in /vagrant/build_scripts/es_setup/elasticsearch_dev.crt -out /vagrant/build_scripts/es_setup/elasticsearch_dev.pem -outform PEM

    sudo service rh-nginx18-nginx restartsudo
fi

mkdir -p /data/es_logs
mkdir -p /data/es_data
chown -R elasticsearch:elasticsearch /data/es_logs /data/es_data
# is this needed?
# chmod 777 -R /data

# 5. Start Elasticsearch
service elasticsearch start

# 6. Add the following lines to /etc/sudoers file
#gpp   ALL=(elasticsearch:elasticsearch) NOPASSWD:ALL
#gpp   ALL=(ALL) NOPASSWD: /etc/init.d/elasticsearch start
#gpp   ALL=(ALL) NOPASSWD: /etc/init.d/elasticsearch stop
#gpp   ALL=(ALL) NOPASSWD: /etc/init.d/elasticsearch status
#gpp   ALL=(ALL) NOPASSWD: /etc/init.d/elasticsearch restart
#gpp   ALL=(ALL) NOPASSWD: /etc/init.d/elasticsearch condrestart
#gpp   ALL=(ALL) NOPASSWD: /etc/init.d/elasticsearch try-restart
#gpp   ALL=(ALL) NOPASSWD: /etc/init.d/elasticsearch reload
#gpp   ALL=(ALL) NOPASSWD: /etc/init.d/elasticsearch force-reload
