from flask import Flask, session

import dj_database_url
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

App = Flask(__name__)
App.config.update(SECRET_KEY=os.urandom(24))
App.config['SESSION_TYPE'] = 'filesystem'

bootstrap = Bootstrap(App)
login_manager=LoginManager()


App.config['SQLALCHEMY_DATABASE_URL']='sqlite:///db.sqlite3'

App.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(App)

from werkzeug.middleware.proxy_fix import ProxyFix
from controllers.authController import*
from controllers.addController import*
from controllers.infoController import*
from controllers.estatisticController import*



App.wsgi_app = ProxyFix(App.wsgi_app, x_proto=1, x_host=1)
if __name__=='__main__':
    App.run(debug=True, host= '192.168.1.12',port=3000)
    App.secret_key = '684651454165416'
    App.config['SESSION_TYPE'] = 'filesystem'

    session.init_app(App)