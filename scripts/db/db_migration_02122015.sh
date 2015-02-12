# Deployment for Database Server - February 10th, 2015
# Description:
# This script performs the following operations:
#	- Sets the ES_HEAP_SIZE to 1/2 of the available RAM in the system
#	- Removes Sample Data from the Database
#	- Fixes missing URLs in the Database
#	- Removes the doc_text column from the dataset
#   - Re-runs the elasticsearch index
# PLEASE NOTE: The script should be run from the folder in which it is contained.

# Store Current Directory
export CWD=$PWD

# Setup Passwords
source ../db/prod.password_store.sh

# Perform Database Migrations
mysql -u root -p$DB_PASS -e "DELETE FROM publications.document WHERE title LIKE '%Sample%' AND agency = 'Aging';"
mysql -u root -p$DB_PASS -e "ALTER TABLE publications.document DROP COLUMN `doc_text`"

# Re-Index the Database
source /var/lib/mysql/virtualenvs/gpp_env/bin/activate
python $CWD/../../application/index_db.py