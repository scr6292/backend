import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
# from flask_migrate import Migrate

Base = declarative_base()

# migrate = Migrate(application, db)


class Contacto(Base):
	__tablename__ = 'contacto'

	id = Column(Integer, primary_key = True)
	email = Column(String(30))
	phone = Column(String(15))
	location = Column(String(80))
	website = Column(String(30))
	procedencia = Column(String(30))

class Agricultor(Base):
	__tablename__ = 'agricultor'

	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	categoria = Column(String(30))
	contacto_id = Column(Integer, ForeignKey('contacto.id'))
	contacto = relationship(Contacto)
	pedido_minimo = (Float(5,2))

class Producto(Base):
	__tablename__ = 'producto'

	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	agricultor_id = Column(Integer, ForeignKey('agricultor.id'))
	agricultor = relationship(Agricultor)


#end of the file 
#Following code is commented just in case willbe usefull in the future
# engine = create_engine(
#		'mysql+pymysql://plantondemand:Fumies9933@plantondemand.cdbbfmyitjua.eu-west-2.rds.amazonaws.com:3306/flaskdb')
#Base.metadata.create_all(engine)

