from application import db
from application.models import Agricultor, Contact, Productos, RegisterForm, LoginForm, User, Pedido, Pickup

db.create_all()

default_pickup = Pickup(name="Default")
db.session.add(default_pickup)
db.session.commit()

default_pickup2 = Pickup(name="Default-2")
db.session.add(default_pickup2)
db.session.commit()

print("DB created.")
