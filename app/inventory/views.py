from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, current_app
from flask.ext.login import login_required
from app.users.models import Users
from app.inventory.forms import ProductForm, OperationForm
from app.inventory.models import Products, Inventory
import datetime


mod = Blueprint('inventory',__name__)


@mod.before_request
def load_menu_data():
    session.activemenu = 'Inventar'


@mod.route('/')
@mod.route('/lista/<value>')
@login_required
def list(value='produse'):

    if value == 'produse':
    	results = [x for x in Products.objects()]
        session.activesubmenu = 'produse'
        return render_template('inventory/list.html', results=results)

    if value == 'operatii':
        results = [x for x in Inventory.objects().order_by('-timestamp')]
        session.activesubmenu = 'operatii'
        return render_template('inventory/oplist.html', results=results)


@mod.route('/adauga/produs/', methods=['GET','POST'])
@login_required
def addproduct():
    form = ProductForm()
    
    if form.validate_on_submit():
        try:
            prod = Products(name=form.name.data,sku=form.sku.data,description=form.description.data,details=form.details.data,stock=0)
            prod.save()
            flash('Produsul a fost adaugat!', category='alert-success')
        except Exception as err:
            flash('Produsul nu poate fi adaugat!', category='alert-warning')
        return redirect(url_for('inventory.list',value='produse'))
    
    return render_template('inventory/add.html',pagetitle='Adauga produs',form=form)


@mod.route('/editeaza/produs/<id>', methods=['GET','POST'])
@login_required
def editproduct(id):
    prod = Products.objects(id=id).get()
    form = ProductForm()

    if form.validate_on_submit():
        try:
            prod.name = form.name.data
            prod.sku = form.sku.data
            prod.description = form.description.data
            prod.details = form.details.data
            prod.save()
            flash('Produsul a fost modificat!', category='alert-success')
        except:
            flash('Produsul nu a putut fi modificat!', category='alert-danger')
        return redirect(url_for('inventory.list',value='produse'))

    form.name.data = prod.name
    form.sku.data = prod.sku
    form.details.data = prod.details
    form.description.data = prod.description

    return render_template('inventory/add.html', pagetitle='Editeaza produs', form=form)


@mod.route('/adauga/operatie', methods=['GET','POST'])
@login_required
def addoperation():
    form = OperationForm()
    form.product.choices = [(x.sku,x.name) for x in Products.objects()]
    if not form.product.choices:
        flash('Nu exista produse!', category='alert-warning')
        return redirect(request.referrer)

    if form.validate_on_submit():
        try:
            prod = Products.objects(sku=form.product.data).get()
            op = Inventory(operation=form.operationtype.data,product=prod,number=form.number.data,timestamp=datetime.datetime.strptime(form.date.data,'%d/%M/%Y'),reference=form.reference.data, operator=g.user)

            if op.operation == 2 and (prod.stock - op.number < 0):
                flash('Operatia nu poate fi facuta! Stock mai mic decat necesar!', category='alert-danger')
                return redirect(request.referrer)

            if op.operation == 1:
                prod.update(inc__stock=op.number)
            else:
                prod.update(dec__stock=op.number)
            op.save()
            flash('Operatia a fost salvata!', category='alert-success')
        except Exception as err:
            print err
            flash('Operatia nu a putut fi salvata!', category='alert-danger')

        return redirect(url_for('inventory.list',value='operatii'))

    return render_template('inventory/add.html', pagetitle='Adauga operatie', form=form)


@mod.route('/ajaxedit/<action>/<value>/<id>')
@login_required
def ajaxedit(action,value,id):

    if value == 'produse' and action == 'delete':
        prod = Products.objects(id=id).get()
        for x in Inventory.objects(product=prod):
            x.delete()
        prod.delete()

    if value == 'operatii' and action == 'delete':
        op = Inventory.objects(id=id).get()
        if op.operation == 1:
            op.product.update(dec__stock=op.number)
        else:
            op.product.update(inc__stock=op.number)
        op.delete()

    return redirect(request.referrer)
