from app import app
import os


username = os.environ.get('DBUSER')
password = os.environ.get('DBPWD')
hostname = os.environ.get('DBHOST')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/publications?charset=utf8' % (username, password, hostname)
app.config['SESSION_COOKIE_NAME'] = 'active'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')