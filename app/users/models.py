from app import db, login_manager
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import datetime


class Users(UserMixin,db.Document):

    username = db.StringField(db_field='un',required=True,unique=True,verbose_name='Nume utilizator')
    avatar = db.ImageField(db_field='ig',verbose_name='Avatar',size=(640,480,True))
    pswd = db.StringField(db_field='ps',required=True)
    joindate = db.DateTimeField(db_field='jd',verbose_name='Data inregistrare',default=datetime.datetime.now())
    email = db.StringField(db_field='em',required=True,unique=True,verbose_name='Email utilizator')
    status = db.BooleanField(db_field='st',verbose_name='Status',default=True)
    permissions = db.StringField(db_field='pm',required=True,verbose_name='Drepturi',default='user')
    specialties = db.ListField(field=db.StringField(),db_field='sp',verbose_name='Specializari')
    interests = db.ListField(field=db.StringField(),db_field='in',verbose_name='Interese')
    projects = db.ListField(field=db.ObjectIdField(),db_field='pj',verbose_name='Proiecte')
    mail_confirmed = db.BooleanField(db_field='mc',default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,passwd):
        self.pswd = generate_password_hash(passwd)

    def verify_password(self,passwd):
        return check_password_hash(self.pswd,passwd)

    def is_admin(self):
        return self.permissions == 'full'

    def is_active(self):
        return self.status

    def generate_confirmation_token(self, expiration=7200):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm': unicode(self.id)})

    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != unicode(self.id):
            return False
        self.mail_confirmed = True
        self.save()
        return True

    def generate_reset_token(self, expiration=7200):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'reset': unicode(self.id)})

    def resetpass(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        if data.get('reset') != unicode(self.id):
            return None
        return self.id


@login_manager.user_loader
def load_user(user_id):
    try:
        user = Users.objects(id=user_id).get()
        return user
    except:
        return None