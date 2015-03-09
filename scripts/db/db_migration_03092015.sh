# Deployment for Database Server - March 9th, 2015
# Description:
# This script performs the following operations:
#   - Re-runs the elasticsearch index
# PLEASE NOTE: The script should be run from the folder in which it is contained.

# Remove old virtualenv
sudo rm -rf /db/mysql_data/virtualenvs/gpp_env

# Create new virtualenv
virtualenv --relocatable /db/mysql_data/virtualenvs/gpp_env

# Index Database
source /db/mysql_data/artifacts/scripts/db/prod.password_store.sh
source /db/mysql_data/virtualenvs/gpp_env/bin/activate
python /db/mysql_data/artifacts/applications/index_db.py
