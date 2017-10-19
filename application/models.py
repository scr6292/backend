from application import db


class Agricultor(db.Model):
	__tablename__ = 'agricultor'

	name = db.Column(db.String(80), nullable = False)
	id = db.Column(db.Integer, primary_key = True)

	def __init__(self, notes):
		self.name = name

	def __repr__(self):
		return '<Agricultor %r>' % self.name


class Producto(db.Model):
	__tablename__ = 'producto'

	name = db.Column(db.String(80), nullable = False)
	id = db.Column(db.Integer, primary_key = True)
	description = db.Column(db.String(250))
	price = db.Column(db.String(8))
	agricultor_id = db.Column(db.Integer, db.ForeignKey('agricultor.id'))
	agricultor = db.relationship(Agricultor)

	def __repr__(self):
		return '<Producto %r>' % self.name

class Contacto(db.Model):
	__tablename__= 'contacto'
	   
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
	
	def __repr__(self):
		return '<Contacto %r>' % self.name
