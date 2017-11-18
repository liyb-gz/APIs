from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
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
        if (mealType is not None) and \
           (location is not None):
            return create_new_restaurant(mealType, location)
        else:
            error_msg = jsonify({
                'error': 'Cannot create the restaurant. Some parameter(s) missing. '
                })
            return error_msg, 404
    elif request.method == 'GET':
        return get_all_restaurant()
    
@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
    if request.method == 'GET':
        return get_restaurant(id)
    elif request.method == 'PUT':
        return update_restaurant(id)
    elif request.method == 'DELETE':
        return delete_restaurant(id)

def create_new_restaurant(mealType, location):
    return 'create new with mealTpye: {}, location: {}'.format(mealType, location)

def get_all_restaurant():
    return 'get all'

def get_restaurant(id):
    return 'get one'

def update_restaurant(id):
    return 'update one'

def delete_restaurant(id):
    return 'delete one'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  
