from application import db
from application.models import Agricultor, Contacto, Producto

db.create_all()

print("DB created.")
