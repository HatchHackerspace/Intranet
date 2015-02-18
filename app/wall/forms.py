from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Required
from wtforms.widgets import TextArea


class PostForm(Form):

	title = StringField(label='Subiect',validators=[Required()])
	content = StringField(label='Continut',validators=[Required()],widget=TextArea())
	submit = SubmitField(label='Posteaza')


class AdminPostForm(Form):

	title = StringField(label='Subiect',validators=[Required()])
	content = StringField(label='Continut',validators=[Required()],widget=TextArea())
	sticky = BooleanField(label='Sticky')
	announce = BooleanField(label='Anunt')
	submit = SubmitField(label='Posteaza')


class CommentForm(Form):

	content = StringField(label='Continut',validators=[Required()],widget=TextArea())
	submit = SubmitField(label='Posteaza')