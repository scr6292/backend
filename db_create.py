from application import db
from application.database_setup import Agricultor, Producto, Contacto

db.create_all()

print("DB created.")
