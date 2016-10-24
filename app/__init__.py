from flask import Flask
from flask.ext.login import LoginManager
import coaster.app

'''
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import config
'''

app = Flask(__name__)
import app.models
from .models import db
import app.views
from config import config

login_manager = LoginManager()
login_manager.session_protection = 'strong'

def init_for(env):
    app.config.from_object(config['development'])
    coaster.app.init_app(app, env)
    login_manager.init_app(app)
    

'''



moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])
    config['development'].init_app(app)
    app.config["SECRET_KEY"] = "SunshineSucks"
    db.init_app()
    login_manager.init_app()
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    return app
    
'''