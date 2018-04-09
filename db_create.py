from application import db
from application.models import Agricultor, Contact, Productos, RegisterForm, LoginForm, User, Pedido

db.create_all()

print("DB created.")
