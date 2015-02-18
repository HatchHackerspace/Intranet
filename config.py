import os, json


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = 'hardtoguesstring'
    MONGODB_SETTINGS = {"DB": "hatchapp","host":"127.0.0.1","port":27017}
    THREADS_PER_PAGE = 8
    CSRF_ENABLED = False
    CSRF_SESSION_KEY = "somethingimpossibletoguess"
    UPLOAD_FOLDER = os.path.join(basedir,'./upload/')
    PERMISSIONS = ['full','user']

    mailcfg = json.load(open('mailcfg.json'))
    MAIL_SERVER = mailcfg['MAIL_SERVER']
    MAIL_PORT = mailcfg['MAIL_PORT']
    MAIL_USE_TLS = mailcfg['MAIL_USE_TLS']
    MAIL_USERNAME = mailcfg['MAIL_USERNAME']
    MAIL_PASSWORD = mailcfg['MAIL_PASSWORD']
    
    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):

    DEBUG = True
    ADMINS = json.load(open('admins.json'))

class ProdConfig(Config):

    DEBUG = False
    ADMINS = json.load(open('admins.json'))

config = {
    'dev':DevConfig,
    'prod':ProdConfig
}