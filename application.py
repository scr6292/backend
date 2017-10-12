'''
Hola Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from application import db
from application.models import Agricultor, Producto, Contacto


# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'q7xsaGX1vwEYfFRV+GTuZP1ISrE8JL7QlkoIAvVe'   

@application.route('/')
def listaAgricultores():
    agriList = db.session.query(Agricultor).all()
    return render_template('agriList.html', agriList = agriList)

@application.route('/agricultores/new', methods=['GET','POST'])
def newListAgricultores():
    if request.method == 'POST':
        newAgri = Agricultor(name = request.form['name'])
        db.session.add(newAgri)
        db.session.commit()
        flash("New agricultor created!")
        return redirect(url_for('listaAgricultores'))
    else:
        return render_template('newagriculture.html')

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


@application.route('/agricultores/<int:agricultor_id>/delete', methods = ['GET', 'POST'])
def deleteAgricultor(agricultor_id):
    selectedItem = db.session.query(Agricultor).filter_by(id = agricultor_id).one()
    if request.method == 'POST':
        db.session.delete(selectedItem)
        db.session.commit()
        flash("Item properly deleted")
        return redirect(url_for('listaAgricultores'))

    else:
        return render_template('deleteagricultor.html', agricultor_id = agricultor_id, item = selectedItem)


@application.route('/agricultores/<int:agricultor_id>/')#
def agricultorMenu(agricultor_id):
    agricultor = db.session.query(Agricultor).filter_by(id=agricultor_id).one()
    items = db.session.query(Producto).filter_by(agricultor_id=agricultor.id)
    return render_template('menu.html', agricultor=agricultor, items=items)

# Task 1: Create route for newMenuItem function here

@application.route('/agricultores/<int:agricultor_id>/new', methods=['GET','POST'])
def newProduct(agricultor_id):
    if request.method == 'POST':
        newItem = Producto(name = request.form['name'], agricultor_id = agricultor_id)
        db.session.add(newItem)
        db.session.commit()
        flash("New menu item created!")
        return redirect(url_for('agricultorMenu', agricultor_id = agricultor_id))
    else:
        return render_template('newmenuitem.html', agricultor_id = agricultor_id)

# Task 2: Create route for editMenuItem function here
@application.route('/agricultores/<int:agricultor_id>/<int:product_id>/edit', methods=['GET', 'POST'])
def editMenuItem(agricultor_id, product_id):
    editedItem = db.session.query(Producto).filter_by(id = product_id).one()
    if request.method == 'POST':
        if request.form['new name']:
            editedItem.name = request.form['new name']
        db.session.add(editedItem)
        db.session.commit()
        flash("Item properly edited")
        return redirect(url_for('agricultorMenu', agricultor_id = agricultor_id))
    else:
        return render_template('editmenuitem.html', agricultor_id = agricultor_id, product_id = product_id, item = editedItem)


# Task 3: Create a route for deleteMenuItem function here
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

# Making an API ENDPOINT (getting menus on JSON)
@application.route('/agricultores/<int:agricultor_id>/menu/JSON')
def restaurantMenuJSON(agricultor_id):
    restaurant = db.session.query(Restaurant).filter_by(id = agricultor_id).one()
    items = db.session.query(MenuItem).filter_by(agricultor_id = agricultor_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)


