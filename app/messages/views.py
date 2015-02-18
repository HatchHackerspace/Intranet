from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, current_app
from flask.ext.login import login_required
from app.users.models import Users
from app.messages.forms import MessageForm
from app.messages.models import Messages
from app.users.decorators import admin_required
from app.services.mail import send_email
from app.services.ajax import getajax, generate_msgid
import datetime


mod = Blueprint('messages',__name__)


@mod.before_request
def load_menu_data():
    session.activemenu = 'Inbox'
    session.usernames = getajax('usernames')


@mod.route('/lista')
@mod.route('/lista/<folder>')
@login_required
def list(folder='inbox'):
    res = [x for x in Messages.objects(ownerid=g.user).order_by('-date,threadid')]

    if folder == 'inbox':
        session.activesubmenu = 'inbox'
        results = [x for x in res if x.folder == 'inbox']
        
    if folder == 'trimise':
        session.activesubmenu = 'trimise'
        results = [x for x in res if x.folder == 'trimise']

    if folder == 'arhiva':
        session.activesubmenu = 'arhiva'
        results = [x for x in res if x.folder == 'arhiva']

    return render_template('messages/list.html',pagetitle=folder,results=results)


@mod.route('/trimite', methods=['GET','POST'])
@mod.route('/trimite/destinatar/<id>', methods=['GET','POST'])
@login_required
def addmessage(id=None,subj=None):
    form = MessageForm()
    if id:
        recp = Users.objects(id=id).get()
        form.recipients.data = recp.username
    
    if form.validate_on_submit():
        if g.user.username in form.recipients.data:
            flash('Expeditorul nu poate fi si destinatar!',category='alert-danger')
            return redirect(request.referrer)
        else:
            recs = []
            for i in form.recipients.data.split(','):
                try:
                    temp_user = Users.objects(username=i).get()
                    recs.append(temp_user)
                except:
                    flash('Utilizatorul '+i+' nu exista!')
                    return redirect(request.referrer)

            msg = Messages(sender=g.user, recipients=recs, title=form.title.data, content=form.content.data, ownerid=g.user, folder='trimise',read=True, msgid=generate_msgid())
            msg.save()
            for i in recs:
                print i.username
                temp = Messages(sender=g.user, recipients=recs, title=form.title.data, content=form.content.data, ownerid=i, folder='inbox', msgid=msg.msgid, date=msg.date)
                temp.save()
            flash('Mesaj trimis!',category='alert-success')
            return redirect(url_for('messages.list'))

    return render_template('messages/add.html',form=form)


@mod.route('/raspunde/<id>', methods=['GET','POST'])
@login_required
def replymessage(id=None):
    form = MessageForm()
    if id:
        tmp = Messages.objects(id=id).get()
        temp_recps = [tmp.sender.username]
        for i in tmp.recipients:
            if i.username != g.user.username:
                temp_recps.append(i.username)
        form.recipients.data = ','.join(temp_recps)
        if 'RE:' not in tmp.title:
            form.title.data = 'RE:'+tmp.title
    else:
        flash('Mesajul nu exista!',category='alert-danger')
        return redirect(request.referrer)
    
    if form.validate_on_submit():
        if g.user.username in form.recipients.data:
            flash('Expeditorul nu poate fi si destinatar!',category='alert-danger')
            return redirect(request.referrer)
        else:
            threadid = Messages.objects(id=id).get().msgid
            recs = []
            for i in form.recipients.data.split(','):
                try:
                    temp_user = Users.objects(username=i).get()
                    recs.append(temp_user)
                except:
                    flash('Utilizatorul '+i+' nu exista!')
                    return redirect(request.referrer)

            msg = Messages(sender=g.user, recipients=recs, title=form.title.data, content=form.content.data, ownerid=g.user, folder='trimise', read=True, threadid=threadid, msgid=generate_msgid())
            msg.save()
            for i in recs:
                temp = Messages(sender=g.user, recipients=recs, title=form.title.data, content=form.content.data, ownerid=i, folder='inbox', msgid=msg.msgid, date=msg.date, threadid=threadid)
                temp.save()
            flash('Mesaj trimis!',category='alert-success')
            return redirect(url_for('messages.list'))

    return render_template('messages/add.html',form=form)


@mod.route('/detalii/<id>')
@login_required
def details(id):
    try:
        msg = Messages.objects(id=id,ownerid=g.user).get()
        if msg.threadid:
            ref_msgs = [x for x in Messages.objects(ownerid=msg.ownerid,threadid=msg.threadid).order_by('-date')]
            ref_msgs += [x for x in Messages.objects(ownerid=msg.ownerid,msgid=msg.threadid).order_by('-date')]
            results = {}
            print len(ref_msgs)
            for n,t in enumerate(ref_msgs):
                results[n] = {"senderlabel":Messages.sender.verbose_name,"sender":t.sender.username,"recipientslabel":Messages.recipients.verbose_name,"recipients":','.join([x.username for x in t.recipients]),"subject":t.title,"content":t.content,"date":t.date,"id":t.id}
        else:
            results = {1:{"senderlabel":Messages.sender.verbose_name,"sender":msg.sender.username,"recipientslabel":Messages.recipients.verbose_name,"recipients":','.join([x.username for x in msg.recipients]),"subject":msg.title,"content":msg.content,"date":msg.date,"id":msg.id}}
        if not msg.read:
            msg.read = True
            msg.save()
    except Exception as err:
        print err
        flash('Nu aveti acces la acest mesaj!')
        return redirect(url_for('messages.list'))

    return render_template('messages/details.html',pagetitle='Detalii mesaj',results=results)


@mod.route('/ajaxedit/<action>/<id>')
@login_required
def ajaxedit(action,id):

    if action == 'markread':
        msg = Messages.objects(ownerid=g.user,id=id).get()
        msg.read = True
        msg.save()

    if action == 'markunread':
        msg = Messages.objects(ownerid=g.user,id=id).get()
        msg.read = False
        msg.save()

    if action == 'delete':
        msg = Messages.objects(ownerid=g.user,id=id).get()
        msg.delete()

    if action == 'archive':
        msg = Messages.objects(ownerid=g.user,id=id).get()
        msg.folder = 'arhiva'
        msg.save()

    return redirect(request.referrer)
