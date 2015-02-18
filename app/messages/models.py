from app import db
import datetime

class Messages(db.Document):

	sender = db.GenericReferenceField(db_field='sd',verbose_name='De la',required=True)
	recipients = db.ListField(db.GenericReferenceField(),db_field='rc',verbose_name='Catre',required=True)
	date = db.DateTimeField(db_field='dt',verbose_name='Data trimitere',default=datetime.datetime.now())
	title = db.StringField(db_field='tl',verbose_name='Subiect')
	content = db.StringField(db_field='ct',verbose_name='Continut')
	read = db.BooleanField(db_field='rd',verbose_name='Status citire',default=False)
	msgid = db.StringField(db_field='mi',verbose_name='Id mesaj',required=True)
	ownerid = db.GenericReferenceField(db_field='ow',verbose_name='Id proprietar mesaj',unique_with='msgid')
	folder = db.StringField(db_field='fl',verbose_name='Folder',choices=['inbox','arhiva','trimise'])
	threadid = db.StringField(db_field='th',verbose_name='Id thread')
		