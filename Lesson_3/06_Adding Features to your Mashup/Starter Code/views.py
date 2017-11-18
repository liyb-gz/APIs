from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, exc
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = '5SI1MULZRJWW5EFUTEPUMYVZJRZ3PAVI0TFQWPJ2XIDLQGEU'
foursquare_client_secret = 'Y3Z5L404OTR5YNQSXTQCWEOTW24EED20XUASGCUBBC0N04EV'
google_api_key = 'AIzaSyDK4XBL7tIg2s1_qqwwp0h2m41gp4O2gPY'

engine = create_engine('sqlite:///restaruants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants/', methods = ['GET', 'POST'])
def all_restaurants_handler():
    if request.method == 'POST':
        mealType = request.args.get('mealType')
        location = request.args.get('location')

        return create_new_restaurant(mealType, location)
    
    elif request.method == 'GET':
        return get_all_restaurant()
    
@app.route('/restaurants/<int:id>/', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
    if request.method == 'GET':
        return get_restaurant(id)

    elif request.method == 'PUT':
        name = request.args.get('name')
        address = request.args.get('address')
        image = request.args.get('image')

        return update_restaurant(id, {
            'name': name,
            'address': address,
            'image': image
        })

    elif request.method == 'DELETE':
        return delete_restaurant(id)

def create_new_restaurant(mealType, location):
    if (mealType is not None) and \
       (location is not None):
        newResInfo = findARestaurant(mealType, location)
        newRes = Restaurant(restaurant_address = newResInfo.get('address'), \
                            restaurant_name = newResInfo.get('name'), \
                            restaurant_image = newResInfo.get('image'))
        session.add(newRes)
        session.commit()
        return jsonify(Restaurant = newRes.serialize)

    else:
        error_msg = jsonify(error = \
            'Cannot create the restaurant. Some parameter(s) missing. ')
        return error_msg, 400

def get_all_restaurant():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants = [res.serialize for res in restaurants])

def get_restaurant(id):
    try:
        res = session.query(Restaurant).filter_by(id = id).one()
        return jsonify(Restaurant = res.serialize)
    except exc.NoResultFound:
        return jsonify(error = 'No restaurant matches the given id.'), 404

def update_restaurant(id, resInfo):
    try:
        res = session.query(Restaurant).filter_by(id = id).one()
        print resInfo

        if all([value is None for value in resInfo.values()]):
            raise ValueError()

        else:
            if resInfo.get('name') is not None:
                res.restaurant_name = resInfo.get('name')

            if resInfo.get('address') is not None:
                res.restaurant_address = resInfo.get('address')

            if resInfo.get('image') is not None:
                res.restaurant_image = resInfo.get('image')

        session.add(res)
        session.commit()

        return jsonify(Restaurant = res.serialize)

    except exc.NoResultFound:
        return jsonify(error = 'No restaurant matches the given id.'), 404

    except ValueError:
        return jsonify(error = 'Cannot update the restaurant. ' + \
                'Missing Parameters.'), 400

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return jsonify(error = message), 404

def delete_restaurant(id):
    return 'delete one'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  
