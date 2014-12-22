# Application Server Setup - Python and Virtualenv Installation
# This script installs Python 2.7.8 in the $HOME/Python-2.7.8 directory and creates
# aliases so that python can be run from the command line
# This script must be run as the local user (admin)
# Please enter the proxy at the beginning of the application

CWD = "$PWD"

# Set Proxy
PROXY = ""
read -p "What is the proxy?" proxy
case $proxy in
	?* ) PROXY = proxy
	* ) echo "Please enter the proxy address";;
esac

# Create alias for sha1sum to prevent scripts from breaking
echo 'alias shasum="sha1sum"' >> $HOME/.bashrc

# Extract the Python tar
tar xvfj ../../install/Python-2.7.8.tar.xz $HOME/python/Python-2.7.8

# Install Python to /usr/local
cd $HOME/python/Python-2.7.8
./configure --prefix=$HOME/python/Python-2.7.8
sudo make && sudo make altinstall

# Add Python to PATH
export PATH=$HOME/python/Python-2.7.8/bin:$PATH

export HTTP_PROXY=PROXY
export HTTPS_PROXY=PROXY
export http_proxy=PROXY
export https_proxy=PROXY

# Install setuptools and pip
cd CWD
sudo python2.7 ../../install/get_pip.py

# Extract the Virtualenv tar
tar zxfj ../../install/virtualenv-1.9.1.tar.gz $HOME/python/virtualenv-1.9.1

# Install virtualenv
cd virtualenv-1.9.1
sudo -E $HOME/Python-2.7.8/bin/python2.7 setup.py install

# Create virtual environments directory
mkdir $HOME/.virtualenvs

