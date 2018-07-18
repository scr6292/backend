from application import db

import datetime
from datetime import date


from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length


# LOGINS

class Pickup(db.Model):
	__tablename__='pickup'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(30),nullable=False)

	def __repr__(self):
		return '<Recogida %r>' % self.name

class User(UserMixin, db.Model):
	__tablename__ = "user"

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), unique=True)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(80))
	user_role = db.Column(db.String(80))
	is_active = db.Column(db.Boolean,default=False)
	is_admin = db.Column(db.Boolean,default=False)
	pickup_id = db.Column(db.Integer, db.ForeignKey('pickup.id'), nullable=False)
	pickup_join = db.relationship(Pickup)



	def __init__(self,username,password,email,user_role,is_active,is_admin,pickup_id):
		self.username = username
		self.password = password
		self.email = email
		self.user_role = user_role
		self.is_active = is_active
		self.is_admin = is_admin
		self.pickup_id = pickup_id

	def get_id(self):
		return self.id
	# def is_active(self):
	# 	return self.is_active
	# def activate_user(self):
	# 	self.is_active = True
	def get_username(self):
		return self.username
	def get_user_role(self):
		return self.user_role
	def get_is_admin(self):
		return self.is_admin
	def get_pickup(self):
		return self.pickup_id

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(message='Introduce un mail'), Email(message='Introduce un mail'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(message='Introduce una password entre 8 y 80 caracteres'), Length(min=8, max=80, message='Introduce una password entre 8 y 80 caracteres')])
    remember = BooleanField('Recordar')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(message='Introduce un mail'), Email(message='Introduce un mail'), Length(max=50)])
    username = StringField('Usuario', validators=[InputRequired(message='Introduce un usuario (entre 8 y 80 caracteres)'), Length(min=4, max=15,message='Introduce un usuario (entre 8 y 80 caracteres)')])
    password = PasswordField('Password', validators=[InputRequired(message='Introduce una password entre 8 y 80 caracteres'), Length(min=8, max=80,message= 'Introduce una password entre 8 y 80 caracteres')])
    pickup = SelectField('Punto de entrega', validators=[InputRequired(message='Por favor, selecciona un punto de recogida')], coerce=int)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.pickup.choices = [(a.id, a.name) for a in db.session.query(Pickup).order_by('name')]

class UpdateUsernameForm(FlaskForm):
    username = StringField('Usuario', validators=[InputRequired(message='Introduce un usuario (entre 8 y 80 caracteres)'), Length(min=4, max=15,message='Introduce un usuario (entre 8 y 80 caracteres)')])

class UpdateEmailForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(message='Introduce un mail'), Email(message='Introduce un mail'), Length(max=50)])

class UpdatePassForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(message='Introduce una password entre 8 y 80 caracteres'), Length(min=8, max=80, message='Introduce una password entre 8 y 80 caracteres')])
# END LOGIN

# OTHER FORMS


#END FORMS

class Agricultor(db.Model):
	__tablename__ = 'agricultor'

	name = db.Column(db.String(80), nullable = False)
	id = db.Column(db.Integer, primary_key = True)

	@property
    	def serialize(self):
    	    return {
           		'name': self.name,
           		'id': self.id
       		}


	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Agricultor %r>' % self.name


class Productos(db.Model):
	#Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
	__tablename__ = 'productos'

	#tell SQLAlchemy the name of column and its attributes:
	product_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	units = db.Column(db.String(80))
	product_title = db.Column(db.String(80))
	location_origin = db.Column(db.String(80))
	unit_price = db.Column(db.Float(8))
	amount = db.Column(db.Float(8))
	current_price = db.Column(db.Float(8))
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	week = db.Column(db.Integer, default=date.today().isocalendar()[1])
	year = db.Column(db.Integer, default=date.today().year)
	agricultor_id = db.Column(db.Integer, db.ForeignKey('agricultor.id'))
	agricultor = db.relationship(Agricultor)

	# pedido_join = db.relationship("Pedido")

	# def __init__(self,product_id,units,product_title,location_origin,unit_price,amount,current_price,created_date,week,year,agricultor_id,agricultor):
	# 	self.product_id = product_id
	# 	self.units = units
	# 	self.product_title = product_title
	# 	self.location_origin = location_origin
	# 	self.unit_price = unit_price
	# 	self.amount = amount
	# 	self.current_price = current_price
	# 	self.created_date = created_date
	# 	self.week = week
	# 	self.year = year
	# 	self.agricultor_id = agricultor_id
	# 	self.agricultor = agricultor

	def __repr__(self):
		return '<Nombre %r>' % self.product_title

	@property
    	def serialize(self):
			return {
				'product_title': self.product_title,
				'units': self.units,
				'product_id': self.product_id,
				'unit_price': self.unit_price,
				'week': self.week,
				'agricultor_id': self.agricultor_id,
			}



class Pedido(db.Model):
	__tablename__= 'pedido'

	id = db.Column(db.Integer, primary_key = True)
	quantity = db.Column(db.String(30))
	product_id = db.Column(db.Integer, db.ForeignKey('productos.product_id'))
	# product_price = db.Column(db.Float(8), db.ForeignKey('productos.unit_price'))
	# product_units = db.Column(db.String(80), db.ForeignKey('productos.units'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	# user_email = db.Column(db.String(50), db.ForeignKey('user.email'), unique=True)
	product_id_join = db.relationship(Productos, foreign_keys=[product_id])	
	# product_price_join = db.relationship(Productos, foreign_keys=[product_price])
	# product_unit_join = db.relationship(Productos, foreign_keys=[product_units])
	user_join = db.relationship(User, foreign_keys=[user_id])
	# user_join = db.relationship(User, foreign_keys=[user_name])
	year = db.Column(db.Integer, default=date.today().year)
	week = db.Column(db.Integer, default=date.today().isocalendar()[1])
	is_confirmed = db.Column(db.Boolean,default=False)

class Contact(db.Model):
	__tablename__= 'contact'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(30),nullable=False)
	phone = db.Column(db.String(15))
	email = db.Column(db.String(30))
	location = db.Column(db.String(80))
	website = db.Column(db.String(30))
	productos = db.Column(db.String(30))
	pedido_minimo = db.Column(db.String(30))
	diasreparto =db.Column(db.String(30))
	logistica= db.Column(db.String(30))
	encargado = db.Column(db.String(30))
	links= db.Column(db.String(30))
	agricultor_id = db.Column(db.Integer, db.ForeignKey('agricultor.id'))
	agricultor = db.relationship(Agricultor)


	@property
    	def serialize(self):
        	return {
        		'id': self.id,
	            'name': self.name,
	            'phone': self.phone,
	            'email': self.email,
	            'location': self.location,
	            'website': self.website,
	            'productos': self.productos,
	            'pedido_minimo': self.pedido_minimo,
	            'diasreparto': self.diasreparto,
	            'logistica': self.logistica,
	            'encargado': self.encargado,
	            'links': self.links,
	            'agricultor_id': self.agricultor_id,



    	    }


	def __repr__(self):
		return '<Contacto %r>' % self.name

