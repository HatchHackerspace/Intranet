from app import db


class WallPosts(db.Document):

	author = db.GenericReferenceField(db_field='au', verbose_name='Autor')
	title = db.StringField(db_field='tl', verbose_name='Titlu')
	content = db.StringField(db_field='ct', verbose_name='Continut', required=True)
	timestamp = db.DateTimeField(db_field='ts', verbose_name='Data')
	sticky = db.BooleanField(db_field='st', verbose_name='Sticky', default=False)
	announce = db.BooleanField(db_field='an', verbose_name='Anunt')
	comments = db.ListField(db.GenericReferenceField(), db_field='cm',verbose_name='Comentarii')


class Comments(db.Document):

	author = db.GenericReferenceField(db_field='au', verbose_name='Autor')
	content = db.StringField(db_field='ct', verbose_name='Continut', required=True)
	timestamp = db.DateTimeField(db_field='ts', verbose_name='Data')
	reference = db.GenericReferenceField(db_field='rf', verbose_name='Referinta')