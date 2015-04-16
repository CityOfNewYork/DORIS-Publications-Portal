# Description:
# This script performs the following operations:
#   - Runs the elasticsearch full text index
# PLEASE NOTE: The script should be run from the folder in which it is contained.

# Source Passwords
source ../db/prod.password_store.sh

# Store Current Directory
export CWD=$PWD

# Run Index
source /var/lib/mysql/virtualenvs/gpp_env/bin/activate
python ../../application/index_full_text_db.py
