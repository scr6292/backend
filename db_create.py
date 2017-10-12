from application import db
from application.models import Contacto, Agricultor, Producto

db.create_all()

print("DB created.")
