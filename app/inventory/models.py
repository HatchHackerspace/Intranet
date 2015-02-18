from app import db


class Products(db.Document):

	name = db.StringField(db_field='nm', required=True, verbose_name='Nume produs')
	sku = db.StringField(db_field='sk', verbose_name='Cod produs')
	description = db.StringField(db_field='ds', verbose_name='Descriere produs')
	details = db.StringField(db_field='dt', verbose_name='Detalii produs')
	stock = db.IntField(db_field='st', verbose_name='Cantitate in stock')


class Inventory(db.Document):

	operation = db.IntField(db_field='on', verbose_name='Tip operatie', required=True)# 1 for buying, 2 for selling
	product = db.ReferenceField('Products',db_field='sk', verbose_name='Produs', required=True)
	number = db.IntField(db_field='nb', verbose_name='Numar produse', required=True)
	timestamp = db.DateTimeField(db_field='tm', verbose_name='Data operatie', required=True)
	reference = db.StringField(db_field='rf', verbose_name='Referinta')
	operator = db.GenericReferenceField(db_field='op', verbose_name='Operator', required=True)
