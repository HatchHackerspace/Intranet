from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, SelectField, ValidationError
from wtforms.validators import Required, EqualTo
from app.users.models import Users


class UserForm(Form):

    username = StringField(label='Nume utilizator', validators=[Required()])
    avatar = FileField(label='Imagine avatar')
    email = StringField(label='Email utilizator', validators=[Required()])
    specialties = StringField(label='Specializari')
    interests = StringField(label='Interese')
    submit = SubmitField('Salveaza')

    def validate_username(self,field):
        try:
            user = Users.objects(username=field.data).get()
            if user:
                raise ValidationError('Utilizatorul exista!')
        except:
            pass
        

    def validate_email(self,field):
        try:
            user = Users.objects(email=field.data).get()
            if user:
                raise ValidationError('Email este deja folosit!')
        except:
            pass


class RegisterForm(Form):

    username = StringField(label='Nume utilizator', validators=[Required()])
    email = StringField(label='Email utilizator', validators=[Required()])
    password = PasswordField(label='Parola', validators=[Required()])
    pass2 = PasswordField(label='Repeta parola', validators=[Required(), EqualTo('password')])
    specialties = StringField(label='Specializari')
    interests = StringField(label='Interese')
    submit = SubmitField('Salveaza')

    def validate_username(self,field):
        try:
            user = Users.objects(username=field.data).get()
            if user:
                raise ValidationError('Utilizatorul exista!')
        except:
            pass
        

    def validate_email(self,field):
        try:
            user = Users.objects(email=field.data).get()
            if user:
                raise ValidationError('Email este deja folosit!')
        except:
            pass


class LoginForm(Form):

    email = StringField(label='Adresa de email', validators=[Required()])
    password = PasswordField(label='Parola', validators=[Required()])
    remember_me = BooleanField(label='Tine-ma minte')
    submit = SubmitField('Login')

class PasswordForm(Form):

    oldpasswd = PasswordField(label='Parola veche',validators=[Required()])
    password = PasswordField(label='Parola noua', validators=[Required()])
    pass2 = PasswordField(label='Repeta parola', validators=[Required(), EqualTo('password')])
    submit = SubmitField('Salveaza')

class ResetPassForm(Form):

    email = StringField(label='Email utilizator', validators=[Required()])
    submit = SubmitField('Trimite')

class NewPassForm(Form):

    password = PasswordField(label='Parola noua', validators=[Required()])
    pass2 = PasswordField(label='Repeta parola', validators=[Required(), EqualTo('password')])
    submit = SubmitField('Salveaza')
