from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from application import db
from application.models import Agricultor, Producto, Contacto

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'q7xsaGX1vwEYfFRV+GTuZP1ISrE8JL7QlkoIAvVe'

#Show all agricultures
@application.route('/')
def listaAgricultores():
    agriList = db.session.query(Agricultor).all()
    return render_template('agriList.html', agriList = agriList)


#Show agricultor info
@application.route('/agricultores/<int:agricultor_id>/info')
def agricultorInfo(agricultor_id):
    agricultor = db.session.query(Agricultor).filter_by(id=agricultor_id).one()
    item = db.session.query(Contacto).filter_by(agricultor_id=agricultor.id).first()
    return render_template('agricultorinfo.html', agricultor=agricultor, item=item)

#Edit agricultor info
@application.route('/agricultores/<int:agricultor_id>/info/edit', methods=['GET', 'POST'])
def editInfo(agricultor_id):
    # agricultor = db.session.query(Agricultor).filter_by(id=agricultor_id).one()
    editedInfo = db.session.query(Contacto).filter_by(agricultor_id = agricultor_id).first()
    if request.method == 'POST':
        if editedInfo:
            if request.form['name']:
                editedInfo.name = request.form['name']
            if request.form['email']:
                editedInfo.email = request.form['email']
            if request.form['phone']:
                editedInfo.phone = request.form['phone']
            if request.form['location']:
                editedInfo.location = request.form['location']
            if request.form['website']:
                editedInfo.website = request.form['website']
            if request.form['productos']:
                editedInfo.productos = request.form['productos']
            if request.form['pedido_minimo']:
                editedInfo.pedido_minimo = request.form['pedido_minimo']
            if request.form['diasreparto']:
                editedInfo.diasreparto = request.form['diasreparto']
            if request.form['logistica']:
                editedInfo.logistica = request.form['logistica']
            if request.form['encargado']:
                editedInfo.encargado = request.form['encargado']
            if request.form['links']:
                editedInfo.links = request.form['links']

            db.session.add(editedInfo)
            db.session.commit()
            flash("Infor properly edited")
            return redirect(url_for('agricultorInfo', agricultor_id = agricultor_id))
        else:    
            editedInfo = Contacto(name = request.form['name'], email =request.form['email'],
                 phone =request.form['phone'], location = request.form['location'],website = request.form['website'],
                 productos = request.form['productos'],pedido_minimo = request.form['pedido_minimo'],
                 diasreparto = request.form['diasreparto'],logistica = request.form['logistica'],
                 encargado = request.form['encargado'],links = request.form['links'],  agricultor_id = agricultor_id)
            db.session.add(editedInfo)
            db.session.commit()
            return redirect(url_for('agricultorInfo', agricultor_id = agricultor_id)) 
    else:
        return render_template('editinfo.html', agricultor_id = agricultor_id, item = editedInfo)
    
        


#Show agricultor products
@application.route('/agricultores/<int:agricultor_id>/')
def agricultorMenu(agricultor_id):
    agricultor = db.session.query(Agricultor).filter_by(id=agricultor_id).one()
    items = db.session.query(Producto).filter_by(agricultor_id=agricultor.id)
    return render_template('menu.html', agricultor=agricultor, items=items)


#Add a new agriculture
@application.route('/agricultores/new', methods=['GET','POST'])
def newAgricultor():
    if request.method == 'POST':
        newAgri = Agricultor(name = request.form['name'])
        db.session.add(newAgri)
        db.session.commit()
        flash("New agricultor created!")
        return redirect(url_for('listaAgricultores'))
    else:
        return render_template('newagriculture.html')

#Edit an agriculture
@application.route('/agricultores/<int:agricultor_id>/edit', methods=['GET', 'POST'])
def editAgricultor(agricultor_id):
    editedAgricultor = db.session.query(Agricultor).filter_by(id = agricultor_id).one()
    if request.method == 'POST':
        if request.form['new name']:
            editedAgricultor.name = request.form['new name']
        db.session.add(editedAgricultor)
        db.session.commit()
        flash("Agricultor properly edited")
        return redirect(url_for('listaAgricultores'))
    else:
        return render_template('editagricultor.html', agricultor_id = agricultor_id, item = editedAgricultor)

#Delete an agricultor
@application.route('/agricultores/<int:agricultor_id>/delete', methods = ['GET', 'POST'])
def deleteAgricultor(agricultor_id):
    selectedContacto = db.session.query(Contacto).filter_by(agricultor_id = agricultor_id).all()
    selectedProducts = db.session.query(Producto).filter_by(agricultor_id = agricultor_id).all()
    selectedItem = db.session.query(Agricultor).filter_by(id = agricultor_id).one()
    if request.method == 'POST':
        for items in selectedProducts:
            db.session.delete(items)
            db.session.commit()
        for items in selectedContacto:
            db.session.delete(items)
            db.session.commit()

        db.session.delete(selectedItem)
        db.session.commit()
        flash("Item properly deleted")
        return redirect(url_for('listaAgricultores'))

    else:
        return render_template('deleteagricultor.html', agricultor_id = agricultor_id, item = selectedItem)


#Add a product
@application.route('/agricultores/<int:agricultor_id>/new', methods=['GET','POST'])
def newProduct(agricultor_id):
    if request.method == 'POST':
        newItem = Producto(name = request.form['name'], description=request.form['description'],
                 price=request.form['price'], agricultor_id = agricultor_id)
        db.session.add(newItem)
        db.session.commit()
        flash("New menu item created!")
        return redirect(url_for('agricultorMenu', agricultor_id = agricultor_id))
    else:
        return render_template('newmenuitem.html', agricultor_id = agricultor_id)


#Edit a product
@application.route('/agricultores/<int:agricultor_id>/<int:product_id>/edit', methods=['GET', 'POST'])
def editMenuItem(agricultor_id, product_id):
    editedItem = db.session.query(Producto).filter_by(id = product_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        db.session.add(editedItem)
        db.session.commit()
        flash("Item properly edited")
        return redirect(url_for('agricultorMenu', agricultor_id = agricultor_id))
    else:
        return render_template('editmenuitem.html', agricultor_id = agricultor_id, product_id = product_id, item = editedItem)


#Delete a product
@application.route('/agricultores/<int:agricultor_id>/<int:product_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(agricultor_id, product_id):
    selectedItem = db.session.query(Producto).filter_by(id = product_id).one()
    if request.method == 'POST':
        db.session.delete(selectedItem)
        db.session.commit()
        flash("Item properly deleted")
        return redirect(url_for('agricultorMenu', agricultor_id = agricultor_id))

    else:
        return render_template('deletemenuitem.html', agricultor_id = agricultor_id, product_id = product_id, item = selectedItem)

# # Making an API ENDPOINT (getting menus on JSON)
# @application.route('/agricultores/<int:agricultor_id>/menu/JSON')
# def restaurantMenuJSON(agricultor_id):
#     restaurant = db.db.session.query(Restaurant).filter_by(id = agricultor_id).one()
#     items = db.db.session.query(MenuItem).filter_by(agricultor_id = agricultor_id).all()
#     return jsonify(MenuItems=[i.serialize for i in items])


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)
