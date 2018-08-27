import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from application import db, application
from application.models import Agricultor, Contact, Pickup, Productos, User, LoginForm, RegisterForm, UpdateUsernameForm, UpdatePassForm, UpdateEmailForm, PickupForm, PickupChoiceForm, PickupHome, Pedido, Order
from werkzeug.utils import secure_filename
import parseCSV
from sqlalchemy import func

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

# Email

from flask import Flask, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


admin = Admin(application)

Bootstrap(application)

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'login'



# test
# SQLALCHEMY_TRACK_MODIFICATIONS = True


#Being able to store files
UPLOAD_FOLDER = '/Users/SRoca/PLANTONDEMAND/November/backend/Documents/csvFiles'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

# Elastic Beanstalk initalization
#application = Flask(__name__)
application.debug=True

# Must be secret
application.secret_key = 'q7xsaGX1vwEYfFRV+GTuZP1ISrE8JL7QlkoIAvVe'

#Set Upload folder
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Email

# application.config.from_pyfile('config.cfg')

application.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'plantondemand@gmail.com',
    MAIL_PASSWORD = '@Fumies9933',
))

mail = Mail(application)

s = URLSafeTimedSerializer(application.secret_key)

# End Email

# LOGIN

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

#Home
@application.route('/', methods=['GET'])
def onepage():
    return redirect(url_for('login'))

#Home
@application.route('/home', methods=['GET'])
def home():
    week = str(date.today().isocalendar()[1])
    return render_template('homepage.html', week = week)


#Order agriculture products
@application.route('/agricultores/<int:agricultor_id>/order', methods=['GET', 'POST'])
@login_required(role="CUSTOMER")
def agricultorMenuOrder(agricultor_id):
    db.session.commit()
    agricultor = db.session.query(Agricultor).filter_by(id=agricultor_id).one()
    items = db.session.query(Productos)
    week = db.session.query(Productos.week).first()
    year = db.session.query(Productos.year).first()
    order = db.session.query(Pedido).filter_by(user_name = current_user.username, week = date.today().isocalendar()[1])
    n_order = db.session.query(Pedido).filter_by(user_name = current_user.username, week = date.today().isocalendar()[1]).count()
    total = 0
    for item in order:
        tot = float(item.product_price)*float(item.quantity)
        total = total + tot
    if request.method == 'POST':
        for item in items:
            try:
                if request.form[item.product_title]:
                    float(request.form[item.product_title].replace(',','.'))
            except:
                numeric = 1
                return render_template('menuOrder.html', agricultor=agricultor, items=items, agricultor_id=agricultor_id, user = current_user.username, week = week, year = year, numeric = numeric, total = total, n_order = n_order)
        for item in items:
            if request.form[item.product_title]:
                already_exist = db.session.query(Pedido).filter_by(product_name = item.product_title, user_name = current_user.username, week = date.today().isocalendar()[1]).first()
                if already_exist:
                    already_exist.quantity = str(float(already_exist.quantity) + float(request.form[item.product_title].replace(',','.')))
                    db.session.add(already_exist)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()

                else:
                    order = Pedido(product_name = item.product_title, quantity = request.form[item.product_title], user_name = current_user.username, email = current_user.email, product_units = item.units, product_price = item.unit_price, week = date.today().isocalendar()[1])
                    db.session.add(order)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()


        order = db.session.query(Pedido).filter_by(user_name = current_user.username, week = date.today().isocalendar()[1]).first()
        if order != None:
            return redirect(url_for('postOrder', agricultor_id = agricultor_id))
        else:
            empty = 1
            return render_template('menuOrder.html', agricultor=agricultor, items=items, agricultor_id=agricultor_id, user = current_user.username, week = week, year = year, empty = empty, total = total, n_order = n_order)

    else:
        return render_template('menuOrder.html', agricultor=agricultor, items=items, agricultor_id=agricultor_id, user = current_user.username, week = week, year = year, total = total, n_order = n_order)
#Post Order page
@application.route('/agricultores/<int:agricultor_id>/postorder', methods=['GET', 'POST'])
@login_required(role="CUSTOMER")
def postOrder(agricultor_id):
    db.session.commit()
    agricultor = db.session.query(Agricultor).filter_by(id=agricultor_id).one()
    weeks = db.session.query(Pedido.week).filter_by(user_name = current_user.username).distinct()
    items = db.session.query(Productos)
    order = db.session.query(Pedido).filter_by(user_name = current_user.username, week = date.today().isocalendar()[1])
    total = 0
    for item in order:
        tot = float(item.product_price)*float(item.quantity)
        total = total + tot
    pointform = PickupForm()
    pickchoice_form = PickupChoiceForm()
    pickupform = PickupHome()
    if request.method == 'POST':
        #TEST
        # if pickchoice_form.validate_on_submit():
        #     pickup = "TEST"
            # pickup = pickchoice_form.pickup.data
            # pickup = pointform.pickup_point.data
        #END TEST
        # if pickchoice_form.pickup.data == "1":
        #     if (total < 25):
        #         pickup_total = 2.0
        #     elif (25 < total < 40):
        #         pickup_total = 1.0
        #     else:
        #         pickup_total = 0.0
        #         pickup = "Recogida en Bustarviejo (Calle Maruste 18)"
        # elif (pickchoice_form.pickup.data == "2"):
        #     if (total < 25):
        #         flash("Para esta modalidad de envio tu pedido debe ser mayor a 25 euros")
        #         return render_template('postOrder.html', agricultor=agricultor, order = order, weeks = weeks, user_name = current_user.username, total = total, pointform = pointform, pickchoice_form = pickchoice_form, pickupform = pickupform)
        #     elif (25 < total < 40):
        #         pickup_total = 2.0
        #     elif (40 < total < 60):
        #         pickup_total = 1.5
        #     else:
        #         pickup_total = 0.0
        #         choice = db.session.query(Pickup).filter_by(id = pointform.pickup_point.data).first()
        #         pickup = choice.name
        # elif (pickchoice_form.pickup.data == "3"):
        #     if (total < 25):
        #         flash("Para esta modalidad de envio tu pedido debe ser mayor a 25 euros")
        #         return render_template('postOrder.html', agricultor=agricultor, order = order, weeks = weeks, user_name = current_user.username, total = total, pointform = pointform, pickchoice_form = pickchoice_form, pickupform = pickupform)
        #     elif (25 < total < 40):
        #         pickup_total = 5.0
        #     elif (40 < total < 60):
        #         pickup_total = 4.0
        #     elif (60 < total < 100):
        #         pickup_total = 3.0
        #     else:
        #         pickup_total = 0.0
        #
        # if (pickupform.street.data != "" and pickupform.city.data != "" and pickupform.cp.data != None):
        #     pickup = pickupform.street.data + ", " + pickupform.city.data + ", " + str(pickupform.cp.data)
        # else:
        #     flash("Por favor introduce datos de entrega")
        #     return render_template('postOrder.html', agricultor=agricultor, order = order, weeks = weeks, user_name = current_user.username, total = total, pointform = pointform, pickchoice_form = pickchoice_form, pickupform = pickupform)

        for item in order:
            try:
                if request.form[item.product_name]:
                    float(request.form[item.product_name].replace(',','.'))
            except:
                numeric = 1
                return render_template('postOrder.html', agricultor=agricultor, order = order, weeks = weeks, user_name = current_user.username, total = total, numeric = numeric)
            for item in order:
                if request.form.get(item.product_name, False):
                    updateorder = db.session.query(Pedido).filter_by(product_name = item.product_name, user_name = current_user.username, week = date.today().isocalendar()[1]).first()
                    updateorder.quantity = request.form[item.product_name]
                    db.session.add(updateorder)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
            #flash("Tus cambios ya estan en el carrito")

        return redirect(url_for('pickup', agricultor_id=agricultor.id))
    #return render_template('postOrder.html', agricultor=agricultor, order = order, weeks = weeks, user_name = current_user.username, total = total, pointform = pointform, pickchoice_form = pickchoice_form, pickupform = pickupform)
    return render_template('postOrder.html', agricultor_id=agricultor_id, order = order, weeks = weeks, user_name = current_user.username, total = total)

@application.route('/agricultores/<int:agricultor_id>/postorder/pickup', methods=['GET','POST'])
@login_required(role="CUSTOMER")
def pickup(agricultor_id):
    db.session.commit()
    agricultor = db.session.query(Agricultor).filter_by(id=agricultor_id).one()
    items = db.session.query(Productos)
    order = db.session.query(Pedido).filter_by(user_name = current_user.username, week = date.today().isocalendar()[1])
    total = 0
    for item in order:
        tot = float(item.product_price)*float(item.quantity)
        total = total + tot
    pointform = PickupForm()
    pickchoice_form = PickupChoiceForm()
    pickupform = PickupHome()

    if request.method == 'POST':
        # TEST
        # pickup = pickchoice_form.pickup.data
        # if pickchoice_form.validate_on_submit():
        #     pickup = "TEST"
        #     pickup = pickchoice_form.pickup.data
        #     pickup = pointform.pickup_point.data
        # END TEST
        if pickchoice_form.pickup.data == "1":
            if (total < 25):
                pickup_total = 2.0
            elif (25 < total < 40):
                pickup_total = 1.0
            else:
                pickup_total = 0.0
            pickup = "Recogida en Bustarviejo (Calle Maruste 18)"
        elif (pickchoice_form.pickup.data == "2"):
            if (total < 25):
                envio = 1
                return render_template('pickup.html', agricultor=agricultor, order = order, user_name = current_user.username, total = total, pointform = pointform, pickchoice_form = pickchoice_form, pickupform = pickupform, envio = envio)
            elif (25 < total < 40):
                pickup_total = 2.0
            elif (40 < total < 60):
                pickup_total = 1.5
            else:
                pickup_total = 0.0
            choice = db.session.query(Pickup).filter_by(id = pointform.pickup_point.data).first()
            pickup = choice.name
        elif (pickchoice_form.pickup.data == "3"):
            if (total < 25):
                envio = 1
                return render_template('pickup.html', agricultor=agricultor, order = order, user_name = current_user.username, total = total, pointform = pointform, pickchoice_form = pickchoice_form, pickupform = pickupform, envio = envio)
            elif (25 < total < 40):
                pickup_total = 5.0
            elif (40 < total < 60):
                pickup_total = 4.0
            elif (60 < total < 100):
                pickup_total = 3.0
            else:
                pickup_total = 0.0
        
            if (pickupform.street.data != "" and pickupform.city.data != "" and pickupform.cp.data != None):
                pickup = pickupform.street.data + ", " + pickupform.city.data + ", " + str(pickupform.cp.data)
            else:
                nodata = 1
                return render_template('pickup.html', agricultor=agricultor, order = order, user_name = current_user.username, total = total, pointform = pointform, pickchoice_form = pickchoice_form, pickupform = pickupform, nodata = nodata)

        return redirect(url_for('orderConfirm', agricultor_id = agricultor_id, pickup = pickup, pickup_total =pickup_total))

    return render_template('pickup.html', agricultor=agricultor, order = order, user_name = current_user.username, total = total, pickupform = pickupform, pickchoice_form = pickchoice_form, pointform = pointform)


@application.route('/agricultores/<int:agricultor_id>/postorder/confirm/<pickup>/<float:pickup_total>', methods=['GET'])
@login_required(role="CUSTOMER")
def orderConfirm(agricultor_id, pickup, pickup_total):
    week = date.today().isocalendar()[1]
    year = date.today().year
    weeks = db.session.query(Pedido.week).filter_by(user_name = current_user.username).distinct()
    order_id = str(week) + str(year) + str(current_user.id)
    new_order = Order(id = order_id, pickup = pickup)

    db.session.commit()
    order = db.session.query(Pedido).filter_by(user_name = current_user.username, week = date.today().isocalendar()[1])
    total = 0
    for item in order:

        tot = float(item.product_price)*float(item.quantity)
        total = total + tot

    total1 = total
    total = total + pickup_total
    new_order.precio_total = total
    try:
        db.session.add(new_order)
        db.session.commit()
    except:
        db.session.rollback()
        doubleorder = 1
        return render_template('postOrder.html', agricultor_id = agricultor_id, doubleorder = doubleorder, order = order, weeks = weeks, user_name = current_user.username, total = total1)

    for item in order:
        item.order_id = order_id
        item.is_confirmed = True
        try:
            db.session.add(item)
            db.session.commit()
        except:
            db.session.rollback()

    msg = Message("Confirmacion de pedido",
                sender="plantondemand@gmail.com",
                recipients=[current_user.email])
    msg.html = render_template('confirmation.html', user_name=current_user.username, total = total, order = order, pickup = pickup, agricultor_id = agricultor_id)
    mail.send(msg)
    return render_template('confirmation.html', user_name = current_user.username, total = total, order = order, pickup = pickup, agricultor_id = agricultor_id, pickup_total = pickup_total)


@application.route('/agricultores/<int:agricultor_id>/postorder/delete/<pedido_id>', methods=['GET','POST'])
@login_required(role="CUSTOMER")
def deleteItem(agricultor_id, pedido_id):

    db.session.commit()
    updateorder = db.session.query(Pedido).filter_by(id = pedido_id, user_name = current_user.username, week = date.today().isocalendar()[1]).first()

    try:
        db.session.delete(updateorder)
        db.session.commit()
    except:
        db.session.rollback()
    return postOrder(agricultor_id)

# Historical Orders
@application.route('/agricultores/<int:agricultor_id>/historicalorder/<int:week>', methods=['GET', 'POST'])
@login_required(role="CUSTOMER")
def historicalOrders(agricultor_id, week):
    db.session.commit()
    agricultor = db.session.query(Agricultor).filter_by(id=agricultor_id).one()
    weeks = db.session.query(Pedido.week).filter_by(user_name = current_user.username).distinct()
    order = db.session.query(Pedido).filter_by(user_name = current_user.username, week = week)
    return render_template('historicalOrders.html', agricultor=agricultor, order = order, weeks = weeks, user_name = current_user.username, week = week)

#Users page
@application.route('/user', methods=['GET', 'POST'])
@login_required(role="CUSTOMER")
def user():
    form_user = UpdateUsernameForm()
    form_pass = UpdatePassForm()
    form_email = UpdateEmailForm()
    currentuser = db.session.query(User).filter_by(username=current_user.username).first()
    if form_user.validate_on_submit():
        if form_user.username.data:
            currentuser.username = form_user.username.data
        db.session.add(currentuser)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return redirect(url_for('user'))
    if form_email.validate_on_submit():
        if form_email.email.data:
            currentuser.email = form_email.email.data
        db.session.add(currentuser)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return redirect(url_for('user'))
    if form_pass.validate_on_submit():
        if form_pass.password.data:
            hashed_password = generate_password_hash(form_pass.password.data, method='sha256')
            currentuser.password = hashed_password
        db.session.add(currentuser)
        try:
            db.session.commit()
        except:
            db.session.rollback() #Rollback the changes on error
        return redirect(url_for('user'))

    return render_template('user.html', formuser=form_user, formpass=form_pass, formemail=form_email)




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


# login


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.is_active == True:
                if check_password_hash(user.password, form.password.data):
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('agricultorMenuOrder', agricultor_id = 1))
                else:
                    invalid_pass = 1
                    return render_template('/login.html',methods=['GET','POST'], form=form, invalid_pass = invalid_pass)
            else:
                link_expired = 1
                user
                return render_template('/login.html',methods=['GET','POST'], form=form, link_expired = link_expired)
                db.session.delete(user)
                db.session.commit()

        else:
            invalid_email = 1
            return render_template('/login.html',methods=['GET','POST'], form=form, invalid_email = invalid_email)

    return render_template('login.html', form=form)

@application.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user_email = User.query.filter_by(email=form.email.data).first()
        user_name = User.query.filter_by(username=form.username.data).first()
        if user_email:
            user_exist = 1
            return render_template('signup.html', form=form, user_exist = user_exist)
        if user_name:
            user_name_exist = 1
            return render_template('signup.html', form=form, user_name_exist = user_name_exist)
        else:
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, is_active=False, user_role="CUSTOMER", is_admin=False)
            db.session.add(new_user)
            try:
                db.session.commit()
            except:
                db.session.rollback()


            email = form.email.data
            token = s.dumps(email, salt='email-confirm')

            msg = Message('Confirm Email', sender='plantondemand@gmail.com', recipients=[email])

            link = url_for('confirm_email', token=token, _external=True)

            msg.body = 'Haz click en el siguiente enlace para confirmar tu cuenta: {}'.format(link)

            mail.send(msg)

            return render_template('confirmation_link.html', email = email)

        # return redirect(url_for('login'))
        # except:
        #     db.session.rollback() #Rollback the changes on error
        #     flash("El email o nombre de usuario que has introducido ya existe, por favor introduce unos distintos")
        #     return redirect(url_for('signup'))



    return render_template('signup.html', form=form)


@application.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        email = s.loads(token, salt='email-confirm')
        user = User.query.filter_by(email=email).first()
        db.session.delete(user)
        db.session.commit()
        return '<h1>Tu link de validacion ha expirado, por favor, registrate de nuevo</h1>'

    user = User.query.filter_by(email=email).first()
    user.is_active = True
    db.session.add(user)
    db.session.commit()

    #flash("Tu email se ha validado correctamente, por favor, inicia sesion")
    return redirect(url_for('login'))
    # # end test email


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
    def is_accessible(self):
        if current_user.user_role == "ADMIN" :
            return True
        else: return False
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

class OrderView(BaseView):

    def is_accessible(self):
        if current_user.user_role == "ADMIN" :
            return True
        else: return False

    @expose('/')
    def pedidos(self):
        order = db.session.query(Pedido).filter_by(week = date.today().isocalendar()[1]).filter_by(is_confirmed=True).group_by(Pedido.user_name).all()
        weeks = db.session.query(Pedido.week).distinct()
        week = db.session.query(Pedido.week).first()
        return self.render('admin/adminorder.html', order = order, weeks = weeks, agricultor_id = 1, week = week)

    @expose('/user/<int:agricultor_id>/<username>/<int:week>')
    def orderuser(self, agricultor_id, username, week):
        db.session.commit()
        agricultor = db.session.query(Agricultor).filter_by(id=agricultor_id).one()
        weeks = db.session.query(Pedido.week).filter_by(user_name = username).distinct()
        order = db.session.query(Pedido).filter_by(user_name = username, week = date.today().isocalendar()[1], is_confirmed = True)
        total = 0
        for item in order:
            tot = float(item.product_price)*float(item.quantity)
            total = total + tot
        return self.render('admin/adminPostOrder.html', agricultor=agricultor, order = order, weeks = weeks, user_name = username, total = total, week = week)


admin.add_view(MyModelView(User ,db.session))
admin.add_view(MyModelView(Productos ,db.session))
admin.add_view(CsvUpdateView(name = 'Actualizar Productos', endpoint = 'csvUpdate'))
admin.add_view(OrderView(name = 'Pedidos', endpoint = 'adminorders'))
admin.add_view(MyModelView(Pickup ,db.session, name = 'Puntos de entrega'))


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)
