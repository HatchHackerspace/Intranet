from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, current_app
from flask.ext.login import login_required
from app.wall.models import WallPosts, Comments
from app.wall.forms import AdminPostForm, PostForm, CommentForm
import datetime


mod = Blueprint('wall',__name__)


@mod.before_request
def load_menu_data():
    session.activemenu = ''


@mod.route('/')
@mod.route('/lista')
@login_required
def list():

	stickies = [x for x in WallPosts.objects(sticky=True).order_by('-timestamp')]
	results = [x for x in WallPosts.objects(sticky=False).order_by('-timestamp')]

	return render_template('wall/list.html', sticky=stickies, results=results)


@mod.route('/adauga/post', methods=['GET','POST'])
@login_required
def addpost():
	if g.user.permissions == 'user':
		form = PostForm()
	if g.user.permissions == 'full':
		form = AdminPostForm()

	if form.validate_on_submit():
		try:
			post = WallPosts(author=g.user, title=form.title.data, content=form.content.data, timestamp=datetime.datetime.now())
			if g.user.permissions == 'full':
				post.sticky = form.sticky.data
				post.announce = form.announce.data
			post.save()
			flash('Postarea a fost salvata!', category='alert-success')
			return redirect(url_for('wall.list'))
		except:
			flash('Postarea nu poate fi salvata!', category='alert-danger')

	return render_template('wall/add.html', form=form, pagetitle='Scrie postare')


@mod.route('/editeaza/post/<id>', methods=['GET','POST'])
@login_required
def editpost(id):
	post = WallPosts.objects(id=id).get()
	if g.user.permissions == 'user':
		form = PostForm()
	if g.user.permissions == 'full':
		form = AdminPostForm()

	if form.validate_on_submit() and (post.author == g.user or g.user.permissions == 'full'):
		try:
			post.title = form.title.data
			post.content = form.content.data
			if g.user.permissions == 'full':
				post.sticky = form.sticky.data
				post.announce = form.announce.data
			post.save()
			flash('Postarea a fost editata!', category='alert-success')
			return redirect(request.args.get('next') or url_for('wall.list'))
		except:
			flash('Postarea nu poate fi editata!', category='alert-danger')

	form.title.data = post.title
	form.content.data = post.content
	if g.user.permissions == 'full':
		form.sticky.data = post.sticky
		form.announce.data = post.announce

	return render_template('wall/add.html', form=form, pagetitle='Editeaza postare')


@mod.route('/detalii/post/<id>')
@login_required
def detailpost(id):
	post = WallPosts.objects(id=id).get()
	comments = [x for x in post.comments]
	form = CommentForm()

	return render_template('wall/details.html', form=form, post=post, results=comments)


@mod.route('/adauga/comentariu/<postid>', methods=['POST'])
@login_required
def addcomment(postid):
	form = CommentForm()

	if form.validate_on_submit():
		try:
			post = WallPosts.objects(id=postid).get()
			comm = Comments(author=g.user, content=form.content.data, reference=post, timestamp=datetime.datetime.now())
			comm.save()
			post.update(add_to_set__comments=comm)
			flash('Comentariul a fost salvat!', category='alert-success')
			return redirect(request.referrer)
		except Exception as err:
			flash('Comentariul nu a putut fi salvat!', category='alert-danger')

	return redirect(request.referrer)


@mod.route('/editeaza/comentariu/<id>', methods=['GET','POST'])
@login_required
def editcomment(id):
	comm = Comments.objects(id=id).get()
	form = CommentForm()

	if form.validate_on_submit():
		try:
			comm.content = form.content.data
			comm.save()
			flash('Comentariul a fost salvat!', category='alert-success')
			return redirect(url_for('wall.detailpost',id=comm.reference.id))
		except:
			flash('Comentariul nu a putut fi salvat!', category='alert-danger')

	form.content.data = comm.content

	return render_template('wall/add.html', form=form, pagetitle='Editeaza comentariu')


@mod.route('/ajaxedit/<action>/<value>/<id>')
@login_required
def ajaxedit(action,value,id):

	if value == 'post':
		field = WallPosts.objects(id=id).get()
	if value == 'comment':
		field = Comments.objects(id=id).get()

	if action == 'delete' and (field.author == g.user or g.user.permissions == 'full'):
		if value == 'comment':
			post = field.reference
			post.update(pull__comments=field)
		field.delete()

	return redirect(request.referrer)


 


