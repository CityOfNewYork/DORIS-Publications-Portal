#!/usr/bin/env bash

# Run after db_setup_install.sh

# populate db
mysql -u root -e "set global net_buffer_length=1000000; set global max_allowed_packet=100000000;"
mysql -u root publications </vagrant/publications.sql

# create user with select permission
mysql -u root -e "GRANT SELECT ON publications.document TO 'index'@'localhost';"

# Index DB
# /home/vagrant/.virtualenvs/gpp/bin/python /vagrant/application/index_db.py