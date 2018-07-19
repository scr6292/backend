import pandas as pd
from numpy import genfromtxt
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from application import db
from application.models import Productos

def Load_Data(file_path):
    data = pd.read_csv(file_path, header=0 )
    numpy_data = data.as_matrix()
    return data

# Base = declarative_base()

# class Productos(Base):
#     #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
#     __tablename__ = 'Productos'
#     __table_args__ = {'sqlite_autoincrement': True}
#     #tell SQLAlchemy the name of column and its attributes:
#     product_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False) 
#     units = Column(String(80))
#     product_title = Column(String(80))
#     location_origin = Column(String(80))
#     unit_price = Column(Float(8))
#     amount = Column(Float(8))
#     current_price = Column(Float(8))

def parsecsv(filename, id):
    t = time()

    # #Create the database
    # engine = create_engine('sqlite:///csv_test.db')
    # Base.metadata.create_all(engine)

    # #Create the session
    # session = sessionmaker()
    # session.configure(bind=engine)
    # s = session()

    try:
        column_names = ['units','product_title','location_origin','unit_price','amount','current_price']
        df=pd.read_csv(open(filename), names=column_names, delimiter=';',skiprows=9, encoding='latin-1')
        # df.to_sql('Productos', engine, if_exists=replace')

        df=df.dropna(thresh=1)

        df['current_price']=df['current_price']
        df['units']=df['units'].str.replace('nan','')
        df['unit_price']=df['unit_price'].str.replace(' _','').str.replace(',','.').astype(float)
        df['current_price']=df['current_price'].str.replace(' _','').str.replace(',','.').astype(float)
        df['amount']=df['amount'].str.replace(',','.').astype(float)
        df['product_title']=df['product_title']
        df['location_origin']=df['location_origin']
        df['product_title']=df['product_title'].str.replace('nan','')
        df['location_origin']=df['location_origin'].str.replace('nan','')
        df['current_price']=df['current_price']
        df['units']=df['units'].str.replace('nan','')

        #df.index.name ='product_id'
        df = df.as_matrix()

        #fill up record var with SQL table data
        for i in df:
        #         print type(i[4])
            record = Productos(**{

                        'units' : i[0],
                        'product_title' : i[1],
                        'location_origin' : i[2],
                        'unit_price' : i[3],
                        # 'amount' : i[4],
                        'current_price' : i[5],
                        'agricultor_id' : id,
            })
            db.session.add(record) #Add all the records
        db.session.commit() #Attempt to commit all the records

    except:
        db.session.rollback() #Rollback the changes on error
    finally:
        Tabla = db.session.query(Productos).all()
        Tabla
        for i in Tabla:
            print i.product_title

        db.session.close() #Close the connection
    print "Time elapsed: " + str(time() - t) + " s." #0.091s

    
    