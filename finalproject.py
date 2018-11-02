from flask import Flask
from flask import render_template, url_for, request, redirect, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


def newsession():
    session = DBSession()
    return session

# TODO: improve API


@app.route('/')
# route show all restaurants
@app.route('/restaurants')
def showRestaurants():
    session = newsession()
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

# add new restaurant


@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    session = newsession()
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'],
                                   description=request.form['description'],
                                   stars=request.form['stars'])
        session.add(newRestaurant)
        session.commit()
        flash("New Restaurant Created!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

# edit a restaurant


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    session = newsession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        restaurant.name = request.form['name']
        restaurant.description = request.form['description']
        restaurant.stars = request.form['stars']
        session.commit()
        flash('Restaurant Successfully Edited')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant=restaurant)

# delete a restaurant


@app.route('/restaurant/<int:restaurant_id>/delete',
           methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    session = newsession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash('Restaurant Successfully Deleted')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant=restaurant)


#  show menu for a restaurant

@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    session = newsession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restuarant_id=restaurant_id)
    print(items)
    return render_template('menu.html', restaurant=restaurant, items=items)

# add an item to the menu


@app.route('/restaurant/<int:restaurant_id>/menu/new',
           methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    session = newsession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['itemname'],
                           description=request.form['description'],
                           price=request.form['price'],
                           course=request.form['course'],
                           restuarant_id=restaurant.id)
        session.add(newItem)
        session.commit()
        flash('New Menu Item Created')
        return redirect(url_for('showMenu', restaurant_id=restaurant.id))
    else:
        return render_template('newMenuItem.html', restaurant=restaurant)

# edit a menu item


@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, item_id):
    session = newsession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        item.name = request.form['itemname']
        item.description = request.form['description']
        item.price = request.form['price']
        item.course = request.form['course']
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('showMenu', restaurant_id=restaurant.id))
    else:
        return render_template('editMenuItem.html', restaurant=restaurant,
                               item=item)

# delete a menu item


@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, item_id):
    session = newsession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showMenu', restaurant_id=restaurant.id))
    else:
        return render_template('deleteMenuItem.html', restaurant=restaurant,
                               item=item)

# API Endpoints

# get all restaurants


@app.route('/restaurants/JSON')
def restaurantsJSON():
    session = newsession()
    restaurants = session.query(Restaurant)
    return jsonify(Restaurants=[i.serialize for i in restaurants])

# get menu items for a restaurant


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    session = newsession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restuarant_id=restaurant_id)
    return jsonify(MenuItems=[i.serialize for i in items])

# get a menu item


@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/JSON')
def menuItemJSON(restaurant_id, item_id):
    session = newsession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
