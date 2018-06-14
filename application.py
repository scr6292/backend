import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from application import db, application
from application.models import Agricultor, Contact, Productos, User, LoginForm, RegisterForm, Pedido
from werkzeug.utils import secure_filename
import parseCSV

# DATES
import datetime
from datetime import date

# LOGIN IMPORT AND SET UP

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from functools import wraps
# Admin
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView

admin = Admin(application)

Bootstrap(application)

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'login'

# Create customized model view class

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
              return login_manager.unauthorized()
            elif (current_user.user_role == "ADMIN"):
                return fn(*args, **kwargs)
            elif ((current_user.user_role != role) and (role != "ANY")):
                return login_manager.unauthorized()
            else:
                return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# END LOGIN



# test
SQLALCHEMY_TRACK_MODIFICATIONS = True




#Being able to store files
UPLOAD_FOLDER = '/Users/SRoca/PLANTONDEMAND/November/backend/Documents/csvFiles'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

# Elastic Beanstalk initalization
#application = Flask(__name__)
application.debug=True

# change this to your own value
application.secret_key = 'q7xsaGX1vwEYfFRV+GTuZP1ISrE8JL7QlkoIAvVe'

#Set Upload folder
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#alloed files
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#Upload csv file
@application.route("/csv/<int:agricultor_id>", methods=['GET', 'POST'])
def csvFiles(agricultor_id):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            parseCSV.parsecsv(filename, agricultor_id)
            return redirect(url_for('csvFiles', agricultor_id = agricultor_id))
    return """
        <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p>%s</p>
    """ % "<br>".join(os.listdir(application.config['UPLOAD_FOLDER'],))

#OnePage
@application.route('/', methods=['GET'])
def onepage():
    return render_template('testSERGI.html')


#Show all agricultures
@application.route('/agricultores', methods=['GET'])
@login_required(role="CUSTOMER")
def listaAgricultores():
    db.session.commit()
    agriList = db.session.query(Agricultor).all()
    return render_template('agriList.html', agriList = agriList)


#Show agricultor info
@application.route('/agricultores/<int:agricultor_id>/info', methods=['GET'])
@login_required(role="CUSTOMER")
def agricultorInfo(agricultor_id):
    db.session.commit()
    agricultor = db.session.query(Agricultor).filter_by(id=agricultor_id).one()
    item = db.session.query(Contact).filter_by(agricultor_id=agricultor.id).first()
    return render_template('agricultorinfo.html', agricultor=agricultor, item=item)

#Edit agricultor info
@application.route('/agricultores/<int:agricultor_id>/info/edit', methods=['GET', 'POST'])
@login_required(role="CUSTOMER")
def editInfo(agricultor_id):
    # agricultor = db.session.query(Agricultor).filter_by(id=agricultor_id).one()
    editedInfo = db.session.query(Contacto).filter_by(agricultor_id = agricultor_id).first()
    if request.method == 'POST':
        if editedInfo:
            if request.form['name']:
                editedInfo.name = request.form['name']
            if request.form['email']:
                editedInfo.email = request.form['email']
            if request.form['phone']:
                editedInfo.phone = request.form['phone']
            if request.form['location']:
                editedInfo.location = request.form['location']
            if request.form['website']:
                editedInfo.website = request.form['website']
            if request.form['productos']:
                editedInfo.productos = request.form['productos']
            if request.form['pedido_minimo']:
                editedInfo.pedido_minimo = request.form['pedido_minimo']
            if request.form['diasreparto']:
                editedInfo.diasreparto = request.form['diasreparto']
            if request.form['logistica']:
                editedInfo.logistica = request.form['logistica']
            if request.form['encargado']:
                editedInfo.encargado = request.form['encargado']
            if request.form['links']:
                editedInfo.links = request.form['links']

            db.session.add(editedInfo)
            try:
                db.session.commit()
            except:
                db.session.rollback() #Rollback the changes on error

            flash("Infor properly edited")
            return redirect(url_for('agricultorInfo', agricultor_id = agricultor_id))
        else:
            editedInfo = Contacto(name = request.form['name'], email =request.form['email'],
                 phone =request.form['phone'], location = request.form['location'],website = request.form['website'],
                 productos = request.form['productos'],pedido_minimo = request.form['pedido_minimo'],
                 diasreparto = request.form['diasreparto'],logistica = request.form['logistica'],
                 encargado = request.form['encargado'],links = request.form['links'],  agricultor_id = agricultor_id)
            db.session.add(editedInfo)
            try:
                db.session.commit()
            except:
                db.session.rollback() #Rollback the changes on error
            return redirect(url_for('agricultorInfo', agricultor_id = agricultor_id))
    else:
        return render_template('editinfo.html', agricultor_id = agricultor_id, item = editedInfo)




#Edit agricultor products
@application.route('/agricultores/<int:agricultor_id>/', methods=['GET'])
@login_required(role="CUSTOMER")
def agricultorMenu(agricultor_id):
    db.session.commit()
    agricultor = db.session.query(Agricultor).filter_by(id=agricultor_id).one()
    items = db.session.query(Productos)
    return render_template('menu.html', agricultor=agricultor, items=items)

#Order agriculture products
@application.route('/agricultores/<int:agricultor_id>/order', methods=['GET', 'POST'])
@login_required(role="CUSTOMER")
def agricultorMenuOrder(agricultor_id):
    db.session.commit()
    agricultor = db.session.query(Agricultor).filter_by(id=agricultor_id).one()
    items = db.session.query(Productos)
    week = db.session.query(Productos.week).first()
    year = db.session.query(Productos.year).first()
    if request.method == 'POST':
        for item in items:
            if request.form[item.product_title]:
                order = Pedido(product_name = item.product_title, quantity = request.form[item.product_title], user_name = current_user.username, email = current_user.email, product_units = item.units, product_price = item.unit_price)
                db.session.add(order)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()

        flash("Tu pedido ha sido procesado!")
        return redirect(url_for('postOrder', agricultor_id = agricultor_id))

    else:
        return render_template('menuOrder.html', agricultor=agricultor, items=items, agricultor_id=agricultor_id, user = current_user.username, week = week, year = year)
#Post Order page
@application.route('/agricultores/<int:agricultor_id>/postorder', methods=['GET', 'POST'])
@login_required(role="CUSTOMER")
def postOrder(agricultor_id):
    db.session.commit()
    agricultor = db.session.query(Agricultor).filter_by(id=agricultor_id).one()
    weeks = db.session.query(Pedido.week).filter_by(user_name = current_user.username).distinct()
    order = db.session.query(Pedido).filter_by(user_name = current_user.username, week = date.today().isocalendar()[1])
    total = 0
    for item in order:
        tot = float(item.product_price)*float(item.quantity)
        total = total + tot
    return render_template('postOrder.html', agricultor=agricultor, order = order, weeks = weeks, user_name = current_user.username, total = total)

# Historical Orders
@application.route('/agricultores/<int:agricultor_id>/historicalorder/<int:week>', methods=['GET', 'POST'])
@login_required(role="CUSTOMER")
def historicalOrders(agricultor_id, week):
    db.session.commit()
    agricultor = db.session.query(Agricultor).filter_by(id=agricultor_id).one()
    weeks = db.session.query(Pedido.week).filter_by(user_name = current_user.username).distinct()
    order = db.session.query(Pedido).filter_by(user_name = current_user.username, week = week)
    return render_template('historicalOrders.html', agricultor=agricultor, order = order, weeks = weeks, user_name = current_user.username, week = week)


#Add a new agriculture
@application.route('/agricultores/new', methods=['GET','POST'])
@login_required(role="CUSTOMER")
def newAgricultor():
    if request.method == 'POST':
        newAgri = Agricultor(name = request.form['name'])
        db.session.add(newAgri)
        try:
            db.session.commit()
        except:
            db.session.rollback() #Rollback the changes on error
        flash("New agricultor created!")
        return redirect(url_for('listaAgricultores'))
    else:
        return render_template('newagriculture.html')

#Edit an agriculture
@application.route('/agricultores/<int:agricultor_id>/edit', methods=['GET', 'POST'])
@login_required(role="CUSTOMER")
def editAgricultor(agricultor_id):
    editedAgricultor = db.session.query(Agricultor).filter_by(id = agricultor_id).one()
    if request.method == 'POST':
        if request.form['new name']:
            editedAgricultor.name = request.form['new name']
        db.session.add(editedAgricultor)
        try:
            db.session.commit()
        except:
            db.session.rollback() #Rollback the changes on error
        flash("Agricultor properly edited")
        return redirect(url_for('listaAgricultores'))
    else:
        return render_template('editagricultor.html', agricultor_id = agricultor_id, item = editedAgricultor)

#Delete an agricultor
@application.route('/agricultores/<int:agricultor_id>/delete', methods = ['GET', 'POST'])
@login_required(role="CUSTOMER")
def deleteAgricultor(agricultor_id):
    selectedContacto = db.session.query(Contacto).filter_by(agricultor_id = agricultor_id).all()
    selectedProducts = db.session.query(Productos).filter_by(agricultor_id = agricultor_id).all()
    selectedItem = db.session.query(Agricultor).filter_by(id = agricultor_id).one()
    if request.method == 'POST':
        for items in selectedProducts:
            db.session.delete(items)
            db.session.commit()
        for items in selectedContacto:
            db.session.delete(items)
            db.session.commit()

        db.session.delete(selectedItem)
        try:
            db.session.commit()
        except:
            db.session.rollback() #Rollback the changes on error
        flash("Item properly deleted")
        return redirect(url_for('listaAgricultores'))

    else:
        return render_template('deleteagricultor.html', agricultor_id = agricultor_id, item = selectedItem)


#Add a product
@application.route('/agricultores/<int:agricultor_id>/new', methods=['GET','POST'])
@login_required(role="CUSTOMER")
def newProduct(agricultor_id):
    if request.method == 'POST':
        newItem = Productos(name = request.form['name'], description=request.form['description'],
                 price=request.form['price'],preciounidad=request.form['preciounidad'], agricultor_id = agricultor_id)
        db.session.add(newItem)
        try:
            db.session.commit()
        except:
            db.session.rollback() #Rollback the changes on error
        flash("New menu item created!")
        return redirect(url_for('agricultorMenu', agricultor_id = agricultor_id))
    else:
        return render_template('newmenuitem.html', agricultor_id = agricultor_id)


#Edit a product
@application.route('/agricultores/<int:agricultor_id>/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required(role="CUSTOMER")
def editMenuItem(agricultor_id, product_id):
    editedItem = db.session.query(Productos).filter_by(product_id = product_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.product_title = request.form['name']
        if request.form['price']:
            editedItem.unit_price = request.form['price']
        if request.form['units']:
            editedItem.units = request.form['units']
        db.session.add(editedItem)
        try:
            db.session.commit()
        except:
            db.session.rollback() #Rollback the changes on error
        flash("Item properly edited")
        return redirect(url_for('agricultorMenu', agricultor_id = agricultor_id))
    else:
        return render_template('editmenuitem.html', agricultor_id = agricultor_id, product_id = product_id, item = editedItem)


#Delete a product
@application.route('/agricultores/<int:agricultor_id>/<int:product_id>/delete', methods = ['GET', 'POST'])
@login_required(role="CUSTOMER")
def deleteMenuItem(agricultor_id, product_id):
    selectedItem = db.session.query(Productos).filter_by(id = product_id).one()
    if request.method == 'POST':
        db.session.delete(selectedItem)
        try:
            db.session.commit()
        except:
            db.session.rollback() #Rollback the changes on error
        flash("Item properly deleted")
        return redirect(url_for('agricultorMenu', agricultor_id = agricultor_id))

    else:
        return render_template('deletemenuitem.html', agricultor_id = agricultor_id, product_id = product_id, item = selectedItem)




# Making an API ENDPOINT (getting agricultors on JSON)
@application.route('/JSON')
def agricultoresJSON():
    agricultors = db.session.query(Agricultor).all()
    return jsonify(Agricultores=[i.serialize for i in agricultors])

# Making an API ENDPOINT (getting products for an agricultor on JSON)
@application.route('/agricultores/<int:agricultor_id>/JSON')
def agricultorProductosJSON(agricultor_id):
    agricultor = db.session.query(Agricultor).filter_by(id = agricultor_id).one()
    items = db.session.query(Productos).filter_by(agricultor_id = agricultor_id).all()
    return jsonify(Products=[i.serialize for i in items])

# Making an API ENDPOINT (getting info for an agricultor on JSON)
@application.route('/agricultores/<int:agricultor_id>/info/JSON')
def agricultorInfoJSON(agricultor_id):
    agricultor = db.session.query(Agricultor).filter_by(id = agricultor_id).one()
    info = db.session.query(Contacto).filter_by(agricultor_id = agricultor_id).one()
    return jsonify(Info=info.serialize)


# LOGIN
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('agricultorMenuOrder', agricultor_id = 1))

        else:
            invalid_pass = 1
            return render_template('/login.html',methods=['GET','POST'], form=form, invalid_pass = invalid_pass)

    return render_template('login.html', form=form)

@application.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, is_active=True, user_role="CUSTOMER", is_admin=False)
        db.session.add(new_user)
        db.session.commit()

        flash("Te has registrado correctamente")
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@application.route('/logout')
@login_required(role="CUSTOMER")
def logout():
    logout_user()
    return redirect(url_for('login'))
# END LOGIN

# ADMIN

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.user_role == "ADMIN" :
            return True
        else: return False

class CsvUpdateView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
                parseCSV.parsecsv(filename, 1)
                return redirect(url_for('admin.index'))

        return self.render('admin/upload_csv.html')


admin.add_view(MyModelView(User ,db.session))
admin.add_view(MyModelView(Productos ,db.session))
admin.add_view(CsvUpdateView(name = 'Actualizar Productos', endpoint = 'csvUpdate'))

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)
