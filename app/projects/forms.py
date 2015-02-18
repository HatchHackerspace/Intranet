from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Required
from wtforms.widgets import TextArea


class ProjectForm(Form):

	title = StringField(label='Subiect',validators=[Required()])
	content = StringField(label='Continut',validators=[Required()],widget=TextArea())
	submit = SubmitField(label='Posteaza')


class ProjPostForm(Form):

	title = StringField(label='Subiect',validators=[Required()])
	content = StringField(label='Continut',validators=[Required()],widget=TextArea())
	submit = SubmitField(label='Posteaza')


class ProjCommentForm(Form):

	content = StringField(label='Continut',validators=[Required()],widget=TextArea())
	submit = SubmitField(label='Posteaza')