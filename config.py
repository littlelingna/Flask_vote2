import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dargun'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:cf123456@127.0.0.1:3306/aero"
#    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:cf123456@127.0.0.1:3306/aero"
    SQLALCHEMY_POOL_SIZE = 5    # SQLAlchemy的连接池大小
    SQLALCHEMY_POOL_TIMEOUT = 15   # SQLAlchemy的连接超时时间
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
