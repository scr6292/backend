from application import db


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
    __tablename__ = 'Productos'

    #tell SQLAlchemy the name of column and its attributes:
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False) 
    units = db.Column(db.String(80))
    product_title = db.Column(db.String(80))
    location_origin = db.Column(db.String(80))
    unit_price = db.Column(db.Float(8))
    amount = db.Column(db.Float(8))
    current_price = db.Column(db.Float(8))
    agricultor_id = db.Column(db.Integer, db.ForeignKey('agricultor.id'))
    agricultor = db.relationship(Agricultor)

	# def __repr__(self):
	# 	return '<Productos %r>' % self.name


class Producto(db.Model):
	__tablename__ = 'producto'

	name = db.Column(db.String(80), nullable = False)
	id = db.Column(db.Integer, primary_key = True)
	description = db.Column(db.String(250))
	price = db.Column(db.String(8))
	preciounidad = db.Column(db.String(8))
	agricultor_id = db.Column(db.Integer, db.ForeignKey('agricultor.id'))
	agricultor = db.relationship(Agricultor)

	@property
    	def serialize(self):
        	return {
	            'name': self.name,
	            'description': self.description,
	            'id': self.id,
	            'price': self.price,
	            'preciounidad': self.preciounidad,
	            'agricultor_id': self.agricultor_id,
	            
    	    }

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
