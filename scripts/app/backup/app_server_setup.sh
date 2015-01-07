# Application Server Setup
# This script installs packages from the RHEL and EPEL Repositories for the Government
# Publications Portal Django Application
# The following packages will be installed:
#  - 'Development Tools' Group
#  - zlib-devel
#  - bzip2-devel
#  - openssl-devel
#  - ncurses-devel
#  - mysql-devel
#  - libxml2-devel
#  - libxslt-devel
#  - unixODBC-devel
#  - sqlite
#  - sqlite-devel
#  - Apache
#  - Nginx
# 
# PLEASE NOTE: This script must be run as the root user on the system.

# Update the server
yum -y update

# Install Packages from RHEL Repositories
yum -y groupinstall "Development tools"
yum -y install zlib-devel
yum -y install bzip2-devel openssl-devel ncurses-devel
yum -y install mysql-devel
yum -y install libxml2-devel libxslt-devel
yum -y install unixODBC-devel
yum -y install sqlite sqlite-devel

# Setup Repos for Nginx
rpm -ivh ../../install/nginx-release-centos-6-0.el6.ngx.noarch.rpm

# Install Nginx
yum -y install nginx