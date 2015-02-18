from app import db


class Projects(db.Document):

	author = db.GenericReferenceField(db_field='au', verbose_name='Autor')
	title = db.StringField(db_field='tl', verbose_name='Titlu')
	content = db.StringField(db_field='ct', verbose_name='Descriere', required=True)
	timestamp = db.DateTimeField(db_field='ts', verbose_name='Data')
	posts = db.ListField(db.GenericReferenceField(), db_field='ps',verbose_name='Postari')
	members = db.ListField(db.GenericReferenceField(), db_field='mb', verbose_name='Participanti')
	applicants = db.ListField(db.GenericReferenceField(), db_field='ap', verbose_name='Aplicatii')


class ProjPosts(db.Document):

	author = db.GenericReferenceField(db_field='au', verbose_name='Autor')
	title = db.StringField(db_field='tl', verbose_name='Titlu')
	content = db.StringField(db_field='ct', verbose_name='Continut', required=True)
	timestamp = db.DateTimeField(db_field='ts', verbose_name='Data')
	project = db.GenericReferenceField(db_field='pr', verbose_name='Proiect')
	comments = db.ListField(db.GenericReferenceField(), db_field='cm',verbose_name='Comentarii')


class ProjComments(db.Document):

	author = db.GenericReferenceField(db_field='au', verbose_name='Autor')
	content = db.StringField(db_field='ct', verbose_name='Continut', required=True)
	timestamp = db.DateTimeField(db_field='ts', verbose_name='Data')
	reference = db.GenericReferenceField(db_field='rf', verbose_name='Referinta')