from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Beverage, beverage_schema, beverages_schema

api = Blueprint('api', __name__, url_prefix='/kitsune')

@api.route('/test')
def hiddenpage():
    return {'fox': 'liquor'}

#Create
@api.route('/brewing', methods = ['POST'])
@token_required
def brew(current_user_token):
    brand = request.json['brand']
    price = request.json['price']
    alcohol_content = request.json['alcohol_content']
    country_origin = request.json['country_origin']
    user_token = current_user_token.token

    print(f'Testing... {current_user_token.token}')

    beverage = Beverage(brand, price, alcohol_content, country_origin, user_token=user_token)
    db.session.add(beverage)
    db.session.commit()

    response = beverage_schema.dump(beverage)
    return jsonify(response)

#View Creations
@api.route('/brewing', methods = ['GET'])
@token_required
def open_fridge(current_user_token):
    a_user = current_user_token.token
    beverages = Beverage.query.filter_by(user_token= a_user).all()
    response = beverages_schema.dump(beverages)
    return jsonify(response)

#View ONE of Your Creations
@api.route('/brewing/<id>', methods = ['GET'])
@token_required
def grab_drink(current_user_token, id):
    beverage = Beverage.query.get(id)
    response = beverage_schema.dump(beverage)
    return jsonify(response)

#Update Creations
@api.route('/brewing/<id>', methods = ['POST', 'PUT'])
@token_required
def update_brewery(current_user_token, id):
    beverage = Beverage.query.get(id)
    beverage.brand = request.json['brand']
    beverage.price = request.json['price']
    beverage.alcohol_content = request.json['alcohol_content']
    beverage.country_origin = request.json['country_origin']
    beverage.user_token = current_user_token.token

    db.session.commit()
    response = beverage_schema.dump(beverage)
    return jsonify(response)

#Delete Creations
@api.route('/brewing/<id>', methods = ['DELETE'])
@token_required
def remove_from_fridge(current_user_token, id):
    beverage = Beverage.query.get(id)
    db.session.delete(beverage)
    db.session.commit()
    response = beverage_schema.dump(beverage)
    return jsonify(response)