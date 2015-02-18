from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, current_app, json
from flask.ext.login import login_user, login_required, logout_user
from app.users.models import Users
from app.users.forms import LoginForm, RegisterForm, UserForm, PasswordForm, ResetPassForm, NewPassForm
from app.users.decorators import admin_required
from app.services.mail import send_email
from app.services.ajax import getnewmessages
import datetime


mod = Blueprint('users',__name__)


@mod.before_app_request
def load_session_data():
    if 'user_id' in session.keys():
        g.user = Users.objects(id=session['user_id']).get()
        session.inbox = getnewmessages(g.user.id)


@mod.before_request
def load_menu_data():
    session.activemenu = 'Membri'
    

@mod.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = Users.objects(email=form.email.data).get()
            if user.verify_password(form.password.data):
                login_user(user,form.remember_me.data)
                return redirect(request.args.get('next') or url_for('wall.list'))
            else:
                raise Exception('Not authorised')
        except Exception as err:
            flash('Invalid username or password!', category='alert-danger')

    return render_template('users/login.html', pagetitle='Login',form=form,login=True)


@mod.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')


@mod.route('/inregistrare', methods=['GET','POST'])
def registeruser():
    """ Build the view used to add new accounts """
    form = RegisterForm()
    
    if form.validate_on_submit():
        try:
            user = Users(username=form.username.data,email=form.email.data,specialties=form.specialties.data.split(','),interests=form.interests.data.split(','))
            user.password = form.password.data
            user.save()
            token = user.generate_confirmation_token()
            send_email(user.email,'Confirmare email','users/email/confirm',user=user,token=token)
            flash('Contul a fost adaugat! Va rugam confirmati adresa de email!', category='alert-success')
        except Exception as err:
            flash('Contul nu poate fi creat!', category='alert-warning')
        return redirect(url_for('users.login'))
    
    return render_template('users/login.html',pagetitle='Inregistrare',form=form,login=False)


@mod.route('/reseteazaparola/', methods=['GET','POST'])
def resetlink():
    form = ResetPassForm()

    if form.validate_on_submit():
        try:
            user = Users.objects(email=form.email.data).get()
            token = user.generate_reset_token()
            send_email(user.email,'Resetare parola','/users/email/passwdreset',user=user,token=token)
            flash('Parola a fost resetata! Va rugam urmati instructiunile primite pe email!',category='alert-success')
            return redirect(request.referrer)
        except Exception as err:
            flash('Adresa de email nu exista!',category='alert-danger')
            return redirect(request.referrer)

    return render_template('users/login.html',pagetitle='Resetare parola',form=form,login=False)


@mod.route('/reseteaza/<email>/<token>', methods=['GET','POST'])
def resetpassword(email,token):
    form = NewPassForm()

    if form.validate_on_submit():
        try:
            user = Users.objects(email=email).get()
            if user.id == user.resetpass(token):
                user.password = form.password.data
                user.save()
                flash('Parola schimbata!',category='alert-success')
                return redirect(url_for('users.login'))
            else:
                raise Exception
        except:
            flash('Token invalid!',category='alert-danger')
            return redirect(url_for('users.resetlink'))

    return render_template('users/login.html',pagetitle='Resetare parola',form=form,login=False)


@mod.route('/confirmaemail/<token>')
@login_required
def confirmemail(token):
    if g.user.mail_confirmed:
        return redirect(request.args.get('next') or url_for('users.edituser'))

    if g.user.confirm(token):
        flash('Adresa de email confirmata!',category='alert-success')
    else:
        flash('Token expirat sau invalid!',category='alert-danger')

    return redirect(request.args.get('next') or url_for('users.edituser'))


@mod.route('/lista')
@login_required
def list():
    """ Build the view used to list all existing accounts """
    results = [x for x in Users.objects()]

    return render_template('users/list.html',results=results)


@mod.route('/adauga', methods=['GET','POST'])
@admin_required
@login_required
def adduser():
    """ Build the view used to add new accounts """
    form = RegisterForm()
    
    if form.validate_on_submit():
        try:
            user = Users(username=form.username.data,email=form.email.data,specialties=form.specialties.data.split(','),interests=form.interests.data.split(','))
            user.password = form.password.data
            user.save()
            token = user.generate_confirmation_token()
            send_email(user.email,'Confirmare email','users/email/confirm',user=user,token=token)
            flash('Contul a fost adaugat!', category='alert-success')
        except Exception as err:
            flash('Utilizatorul are deja cont!', category='alert-warning')
        return redirect(url_for('users.list'))
    
    return render_template('users/add.html',pagetitle='Adauga utilizator',form=form)


@mod.route('/editeaza/', methods=['GET','POST'])
@login_required
def edituser():
    """ Build the view used to edit existing accounts """
    user = Users.objects(id=unicode(g.user.id)).get()
    form = UserForm()
    
    if form.validate_on_submit():
        user.username = form.username.data
        if form.avatar.data:
            image_data = request.FILES[form.avatar.name].read()
            user.avatar = image_data
        user.email = form.email.data
        user.specialties = form.specialties.data.split(',')
        user.interests = form.interests.data.split(',')
        user.save()
        flash('Cont modificat!',category='alert-success')
        return redirect(request.referrer)

    form.username.data = user.username
    form.email.data = user.email
    form.avatar.data = ''
    form.specialties.data = ','.join(user.specialties)
    form.interests.data = ','.join(user.interests)
            
    return render_template('users/add.html',pagetitle='Editeaza utilizator',form=form)



@mod.route('/editeazaparola/', methods=['GET','POST'])
@login_required
def editpswduser():
    """ Build the view used to edit a password for an existing account """
    user = Users.objects(id=unicode(g.user.id)).get()
    form = PasswordForm()
    
    if form.validate_on_submit() and user.verify_password(form.oldpasswd.data):
        user.password = form.password.data
        user.save()
        flash('Parola modificata!', category='alert-success')
        return redirect(request.referrer)
    
    return render_template('users/add.html',pagetitle='Editeaza parola',form=form)


@mod.route('/detalii/<id>')
@login_required
def detailuser(id):
    user = Users.objects(id=id).get()
    results = [(Users.username.verbose_name,user.username),(Users.specialties.verbose_name,','.join(user.specialties)),(Users.interests.verbose_name,','.join(user.interests))]

    return render_template('users/details.html',pagetitle='Detalii utilizator',results=results)


@mod.route('/ajaxedit/<action>/<id>', methods=['GET'])
@admin_required
@login_required
def ajaxedit(action,id):
    user = Users.objects(id=id).get()

    if action == 'delete' and id != unicode(g.user.id):
        user.delete()

    if action == 'mkadmin' and id != unicode(g.user.id):
        user.permissions = 'full'
        user.save()

    if action == 'mkuser' and id != unicode(g.user.id):
        user.permissions = 'user'
        user.save()

    if action == 'deactivate' and id != unicode(g.user.id):
        user.status = False
        user.save()

    if action == 'activate' and id != unicode(g.user.id):
        user.status = True
        user.save()

    return redirect(request.referrer)