from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from wtforms.widgets import TextArea


class MessageForm(Form):

	recipients = StringField(label='Catre:',validators=[Required()])
	title = StringField(label='Subiect',validators=[Required()])
	content = StringField(label='Continut',validators=[Required()],widget=TextArea())
	submit = SubmitField(label='Trimite')
