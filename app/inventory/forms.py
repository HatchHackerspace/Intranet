from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import Required
from wtforms.widgets import TextArea


class ProductForm(Form):
	
	name = StringField(label='Nume produs', validators=[Required()])
	sku = StringField(label='Cod produs', validators=[Required()])
	description = StringField(label='Descriere', validators=[Required()])
	details = StringField(label='Detalii', widget=TextArea())
	submit = SubmitField(label='Salveaza')


class OperationForm(Form):

	operationtype = SelectField(label='Tip de operatie', validators=[Required()], choices=[(1,'Intrare'),(2,'Iesire')], coerce=int)
	product = SelectField(label='Produs', validators=[Required()], coerce=str)
	number = IntegerField(label='Cantitate', validators=[Required()])
	reference = StringField(label='Referinta', widget=TextArea())
	date = StringField(label='Data operatie', validators=[Required()])
	submit = SubmitField(label='Salveaza')