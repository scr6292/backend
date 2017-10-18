import os
import sys
from flask import Flask
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

# -------------------------------------------------------------------------------
# config.py
#
# edit the URI below to add your RDS password and your AWS URL
# The other elements are the same as used in the tutorial
# format: (user):(password)@(db_identifier).amazonaws.com:3306/(db_name)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://plantondemand:Fumies9933@ec2-35-176-159-65.eu-west-2.compute.amazonaws.com:3306/agricultores'

# Uncomment the line below if you want to work with a local DB
#SQLALCHEMY_DATABASE_URI = 'sqlite:///Test1.db'

SQLALCHEMY_POOL_RECYCLE = 3600

WTF_CSRF_ENABLED = True
SECRET_KEY = 'q7xsaGX1vwEYfFRV+GTuZP1ISrE8JL7QlkoIAvVe'
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------

class Agricultor(Base):
	__tablename__ = 'agricultor'

	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	# categoria = Column(String(30))
	# pedido_minimo = Column(String(8))
	

class Contacto(Base):
	__tablename__ = 'contacto'

	id = Column(Integer, primary_key = True)
	name = Column(String(30),nullable=False)
	phone = Column(String(15))
	email = Column(String(30))
	location = Column(String(80))
	website = Column(String(30))
	productos = Column(String(30))
	pedido_minimo = Column(String(30))
	diasreparto =Column(String(30))
	logistica= Column(String(30))
	encargado = Column(String(30))
	links= Column(String(30))
	agricultor_id = Column(Integer, ForeignKey('agricultor.id'))
	agricultor = relationship(Agricultor)


class Producto(Base):
	__tablename__ = 'producto'

	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	description = Column(String(250))
	price = Column(String(8))
	agricultor_id = Column(Integer, ForeignKey('agricultor.id'))
	agricultor = relationship(Agricultor)



# -------------------------------------------------------------------------------

engine = create_engine(SQLALCHEMY_DATABASE_URI)

Base.metadata.create_all(engine)
