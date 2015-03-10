# Migration for Database Server - March 10th, 2015
# Description:
# This script performs the following functions:
#	- Updates the Database
#	- Re-Runs Elasticsearch Index
# PLEASE NOTE: This script should be run from the folder in which it is contained.

# Source Passwords
source prod.password_store.sh

# Backup and Empty Database
mysqldump -u root -p$DB_PASS publications > /db/mysql_data/publications_03102015.sql
mysql -u root -p$DB_PASS -e "DROP SCHEMA publications; CREATE DATABASE publications;"

# Import new data
mysql -u root -p$DB_PASS publications < ../../publications.sql

# Run Index
source /db/mysql_data/virtualenvs/gpp_env/bin/activate
python ../../application/index_db.py