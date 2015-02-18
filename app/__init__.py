from flask import Flask, render_template, redirect, url_for
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from config import config


bootstrap = Bootstrap()
moment = Moment()
db = MongoEngine()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'users.login'
mail = Mail()


def create_admins(admin):

    from app.users.models import Users
    
    try:
        user = Users.objects(email=admin['email']).get()
    except:
        user = Users(email=admin['email'],username=admin['username'],permissions='full',status=True)
        user.password = admin['password']
        user.save()


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.session_interface = MongoEngineSessionInterface(db)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    create_admins(config[config_name].ADMINS)

    #errorhandlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    #routes
    @app.route('/login', methods=['GET','POST'])
    def loginpage():
        return redirect(url_for('users.login'))

    @app.route('/')
    @app.route('/home')
    def homepage():
        return redirect(url_for('wall.list'))

    #filters
    @app.template_filter('boolswitch')
    def switchboolean(s):
        var = {True:'DA',False:'NU'}
        return var[s]

    
    from .users.views import mod as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/membri')
    from .messages.views import mod as msgs_blueprint
    app.register_blueprint(msgs_blueprint, url_prefix='/mesagerie')
    from .wall.views import mod as wall_blueprint
    app.register_blueprint(wall_blueprint, url_prefix='/home')
    from .projects.views import mod as proj_blueprint
    app.register_blueprint(proj_blueprint, url_prefix='/proiecte')
    from .inventory.views import mod as inv_blueprint
    app.register_blueprint(inv_blueprint, url_prefix='/inventar')
   
    return app