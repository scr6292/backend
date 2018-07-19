from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__, template_folder='../templates')
application = Flask(__name__, static_url_path='../application/static')

application.config.from_object('config')
db = SQLAlchemy(application)
