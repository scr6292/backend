from application import db
from application.models import Agricultor, Contact, Productos, RegisterForm, LoginForm, User, Pedido, Pickup

db.create_all()

default_pickup = Pickup(name="Default")
db.session.add(default_pickup)
db.session.commit()

admin = User(username='Admin', email='admin@admin.com', password='sha256$RiJPq3hT$74f39e5334d7650bfb30e8294aac9b4275d304507e0e140abc2bec7c6ecebf50', is_active=True, user_role="ADMIN", is_admin=True, pickup='Default')
db.session.add(admin)
db.session.commit()


default_agri = Agricultor(name = "Nuestras Huertas")
db.session.add(default_agri)
db.session.commit()


print("DB created.")
