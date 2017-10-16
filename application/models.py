from application import db


class Contacto(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(30))
	email = db.Column(db.String(30), nullable=False)
	phone = db.Column(db.String(15), nullable=False)
	location = db.Column(db.String(80))
	website = db.Column(db.String(30))
	procedencia = db.Column(db.String(30))
	
	def __repr__(self):
		return '<Contacto %r>' % self.email

class Agricultor(db.Model):
	__tablename__ = 'agricultor'

	name = db.Column(db.String(80), nullable = False)
	id = db.Column(db.Integer, primary_key = True)
	categoria = db.Column(db.String(30))
	contactoId = db.Column(db.Integer, db.ForeignKey('contacto.id'))
	contacto = db.relationship(Contacto)
	pedidoMinimo = (db.Float(5,2))
	
	def __repr__(self):
		return '<Agricultor %r>' % self.name

class Producto(db.Model):
	__tablename__ = 'producto'

	name = db.Column(db.String(80), nullable = False)
	id = db.Column(db.Integer, primary_key = True)
	course = db.Column(db.String(250))
	description = db.Column(db.String(250))
	price = db.Column(db.String(8))
	agricultor_id = db.Column(db.Integer, db.ForeignKey('agricultor.id'))
	agricultor = db.relationship(Agricultor)

	def __repr__(self):
		return '<Producto %r>' % self.name