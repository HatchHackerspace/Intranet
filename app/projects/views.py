from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, current_app
from flask.ext.login import login_required
from app.projects.models import Projects, ProjPosts, ProjComments
from app.projects.forms import ProjectForm, ProjPostForm, ProjCommentForm
import datetime


mod = Blueprint('projects',__name__)


@mod.before_request
def load_menu_data():
    session.activemenu = 'Proiecte'
    

@mod.route('/')
@mod.route('/lista')
@login_required
def list():

	results = [x for x in Projects.objects().order_by('-timestamp')]

	return render_template('projects/list.html', results=results)


@mod.route('/adauga/', methods=['GET','POST'])
@login_required
def addproject():
	form = ProjectForm()

	if form.validate_on_submit():
		try:
			proj = Projects(author=g.user, title=form.title.data, content=form.content.data, timestamp=datetime.datetime.now(), members=[g.user])
			proj.save()
			flash('Proiectul a fost salvat!', category='alert-success')
			return redirect(url_for('projects.list'))
		except:
			flash('Proiectul nu poate fi salvat!', category='alert-danger')

	return render_template('projects/add.html', form=form, pagetitle='Adauga proiect')


@mod.route('/editeaza/proiect/<id>', methods=['GET','POST'])
@login_required
def editproject(id):
	proj = Projects.objects(id=id).get()

	if form.validate_on_submit() and (proj.author == g.user or g.user.permissions == 'full'):
		try:
			proj.title = form.title.data
			proj.content = form.content.data
			proj.save()
			flash('Proiectul a fost editat!', category='alert-success')
			return redirect(request.args.get('next') or url_for('project.list'))
		except:
			flash('Proiectul nu poate fi editat!', category='alert-danger')

	form.title.data = proj.title
	form.content.data = proj.content

	return render_template('projects/add.html', form=form, pagetitle='Editeaza proiect')


@mod.route('/detalii/proiect/<id>')
@login_required
def detailproject(id):
	proj = Projects.objects(id=id).get()
	posts = [x for x in proj.posts]
	applicants = [x for x in proj.applicants]
	
	return render_template('projects/details.html', post=proj, results=posts)


@mod.route('/proiect/<id>/aplica')
@login_required
def applyproject(id):
	proj = Projects.objects(id=id).get()
	proj.update(add_to_set__applicants=g.user)
	flash('Aplicatia ta a fost inregistrata si asteapta sa fie validata de catre un membru al proiectului!', category='alert-success')

	return redirect(request.referrer)


@mod.route('/proiect/<id>/renunta')
@login_required
def leaveproject(id):
	proj = Projects.objects(id=id).get()
	if len(proj.members) == 1:
		flash('Esti singurul membru al proiectului!', category='alert-danger')
	else:
		if g.user in proj.members:
			proj.update(pull__members=g.user)
			if g.user == proj.author:
				proj.update(set__author=proj.members[0])
		if g.user in proj.applicants:
			proj.update(pull__applicants=g.user)

	return redirect(request.referrer)


@mod.route('/proiect/<id>/aplicant/<apid>/<action>')
@login_required
def applicantmod(id,apid,action):
	proj = Projects.objects(id=id).get()
	if g.user not in proj.members:
		flash('Nu poti face aceasta operatie!', category='alert-danger')
		return redirect(request.referrer)
	else:
		for x in proj.applicants:
			if unicode(x.id) == apid: 
				if action == 'accept':
					proj.update(push__members=x)
				proj.update(pull__applicants=x)

	return redirect(request.referrer)


@mod.route('/proiect/<id>/adauga/post', methods=['GET','POST'])
@login_required
def addpost(id):
	proj = Projects.objects(id=id).get()
	form = ProjPostForm()

	if form.validate_on_submit() and g.user in proj.members:
		try:
			post = ProjPosts(author=g.user, title=form.title.data, content=form.content.data, timestamp=datetime.datetime.now(), project=proj)
			post.save()
			proj.update(add_to_set__posts=post)
			flash('Postarea a fost salvata!', category='alert-success')
			return redirect(url_for('projects.detailproject',id=proj.id))
		except:
			flash('Postarea nu poate fi salvata!', category='alert-danger')

	return render_template('wall/add.html', form=form, pagetitle='Scrie postare')


@mod.route('/proiect/editeaza/post/<id>', methods=['GET','POST'])
@login_required
def editpost(id):
	post = ProjPosts.objects(id=id).get()
	form = ProjPostForm()

	if form.validate_on_submit() and g.user in proj.members:
		try:
			post.title = form.title.data
			post.content = form.content.data
			post.save()
			flash('Postarea a fost editata!', category='alert-success')
			return redirect(request.args.get('next') or url_for('projects.list'))
		except:
			flash('Postarea nu poate fi editata!', category='alert-danger')

	form.title.data = post.title
	form.content.data = post.content
	
	return render_template('wall/add.html', form=form, pagetitle='Editeaza postare')


@mod.route('/proiect/detalii/post/<id>')
@login_required
def detailpost(id):
	post = ProjPosts.objects(id=id).get()
	comments = [x for x in post.comments]
	form = ProjCommentForm()

	return render_template('projects/postdetails.html', form=form, post=post, results=comments)


@mod.route('/proiect/postare/<postid>/adauga/comentariu', methods=['POST'])
@login_required
def addcomment(postid):
	post = ProjPosts.objects(id=postid).get()
	form = ProjCommentForm()

	if form.validate_on_submit():
		try:
			comm = ProjComments(author=g.user, content=form.content.data, reference=post, timestamp=datetime.datetime.now())
			comm.save()
			post.update(add_to_set__comments=comm)
			flash('Comentariul a fost salvat!', category='alert-success')
			return redirect(request.referrer)
		except Exception as err:
			print err
			flash('Comentariul nu a putut fi salvat!', category='alert-danger')

	return redirect(request.referrer)


@mod.route('/proiect/postare/editeaza/comentariu/<id>', methods=['GET','POST'])
@login_required
def editcomment(id):
	comm = ProjComments.objects(id=id).get()
	form = ProjCommentForm()

	if form.validate_on_submit():
		try:
			comm.content = form.content.data
			comm.save()
			flash('Comentariul a fost salvat!', category='alert-success')
			return redirect(url_for('projects.detailpost',id=comm.reference.id))
		except:
			flash('Comentariul nu a putut fi salvat!', category='alert-danger')

	form.content.data = comm.content

	return render_template('wall/add.html', form=form, pagetitle='Editeaza comentariu')


@mod.route('/proiect/ajaxedit/<action>/<value>/<id>')
@login_required
def ajaxedit(action,value,id):

	if value == 'post':
		field = ProjPosts.objects(id=id).get()
	if value == 'comment':
		field = ProjComments.objects(id=id).get()
	if value == 'proj':
		field = Projects.objects(id=id).get()

	if action == 'delete' and (field.author == g.user or g.user.permissions == 'full'):
		if value == 'comment':
			post = field.reference
			post.update(pull__comments=field)
		if value == 'post':
			for f in field.comments:
				f.delete()
		if value == 'proj':
			for t in field.posts:
				for f in field.comments:
					f.delete() 
				t.delete()
		field.delete()


	return redirect(request.referrer)


