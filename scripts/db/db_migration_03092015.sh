# Deployment for Database Server - March 9th, 2015
# Description:
# This script performs the following operations:
#   - Re-runs the elasticsearch index
# PLEASE NOTE: The script should be run from the folder in which it is contained.

# Store Current Directory
export CWD=$PWD

# Setup Passwords
source $CWD/prod.password_store.sh

# Re-Index the Database
source /db/mysql_data/virtualenvs/gpp_env/bin/activate
python $CWD/../../application/index_db.py
