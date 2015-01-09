# ElasticSearch Setup

CURRENT_DIR = $PWD

# Move ElasticSearch.yml to correct directory
mv /etc/elastisearch/elastisearch.yml /etc/elastisearch/elastisearch.yml.orig
cp ../../conf/elastisearch.yml /etc/elastisearch/config

# Install Elasticsearch Head
cp ../../install/elasticsearch-head /home/mysql/es_plugins/

# Set HeapSize
export ES_HEAP_SIZE=10g

# Set Min and Max Mem
export ES_MIN_MEM = 512m
export ES_MAX_MEM = 512m

# Setup HTTPS Authentication
sudo mkdir /etc/elasticsearch/ssl
cd /etc/elasticsearch/ssl

# Generate Password
PASSWORD = openssl rand -base64 32

# Generate Key
openssl genrsa -des3 -out es_domain.key 1024
expect "Enter pass phrase for es_domain.key:"
send $PASSWORD
expect "Verifying - Enter pass phrase for es_domain.key:"
send PASSWORD

openssl req -new -key es_domain.key -out es_domain.csr

# Start Elasticsearch
service elasticsearch start