#!/usr/bin/env bash

# 11. Create postgres users
sudo -u postgres /opt/rh/rh-postgresql95/root/usr/bin/createuser -s -e developer
sudo -u postgres /opt/rh/rh-postgresql95/root/usr/bin/createuser -s -e gpp_db

# 12. Create database
sudo -u postgres /opt/rh/rh-postgresql95/root/usr/bin/createdb gpp

# 13. Add the following lines to /etc/sudoers file (allows running postgres commands without sudo access)
#vagrant  ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql start
#vagrant  ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql stop
#vagrant  ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql status
#vagrant  ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql restart
#vagrant  ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql condrestart
#vagrant  ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql try-restart
#vagrant  ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql reload
#vagrant  ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql force-reload
#vagrant  ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql initdb
#vagrant  ALL=(ALL) NOPASSWD: /etc/init.d/rh-postgresql95-postgresql upgrade
