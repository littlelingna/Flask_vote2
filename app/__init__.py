# coding: utf-8

from flask import Flask, request
from os import path
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,current_user
# from flask_pagedown import PageDown
#from flask_gravatar import Gravatar
#from flask_babel import Babel, gettext as _
from config import config

basedir = path.abspath(path.dirname(__file__))

db = SQLAlchemy()
#babel = Babel()
bootstrap = Bootstrap()
# pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

## 初始化app

    bootstrap.init_app(app)
    login_manager.init_app(app)
    # pagedown.init_app(app)

    # babel.init_app(app)
    # Gravatar(app, size=64)

## 注册blueprint
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint, static_folder='static')


    # config[config_name].init_app(app)
    # bootstrap.init_app(app)
    # mail.init_app(app)
    # moment.init_app(app)

#临时添加db config
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:cf123456@127.0.0.1:3306/aero?charset=utf8"
    app.config["SQLALCHEMY_POOL_SIZE"] = 5    # SQLAlchemy的连接池大小
    app.config["SQLALCHEMY_POOL_TIMEOUT"] = 15   # SQLAlchemy的连接超时时间
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)



    return app
