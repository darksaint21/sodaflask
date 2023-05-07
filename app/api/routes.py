from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, User, Soda, soda_schema, sodas_schema

api = Blueprint('api', __name__, url_prefix='/api')


# GET routes
@api.route('/sodas')
@token_required
def get_sodas(current_user_token):
    user = current_user_token.token
    sodas = Soda.query.filter_by(user_token = user).all()
    response = sodas_schema.dump(sodas)
    return jsonify(response)


@api.route('/sodas/<id>')
@token_required
def get_soda(current_user_token, id):
    soda = Soda.query.get(id)
    response = soda_schema.dump(soda)
    return jsonify(response)


# POST routes
@api.route('/sodas', methods = ['POST'])
@token_required
def create_soda(current_user_token):
    brand = request.json['brand']
    flavor = request.json['flavor']
    size = request.json['size']
    diet = request.json['diet']
    cost = request.json['cost']
    user_token = current_user_token.token
    
    soda = Soda(brand, flavor, size, cost, user_token, diet)
    
    db.session.add(soda)
    db.session.commit()
    
    response = soda_schema.dump(soda)
    return jsonify(response)


# PUT routes
@api.route('/sodas/<id>', methods = ['PUT'])
@token_required
def update_soda(current_user_token, id):
    soda = Soda.query.get(id)
    soda.brand = request.json['brand']
    soda.flavor = request.json['flavor']
    soda.size = request.json['size']
    soda.diet = request.json['diet']
    soda.cost = request.json['cost']
    soda.user_token = current_user_token.token
    
    db.session.commit()
    
    response = soda_schema.dump(soda)
    return jsonify(response)


# DELETE routes
@api.route('/sodas/<id>', methods = ['DELETE'])
@token_required
def delete_soda(current_user_token, id):
    soda = Soda.query.get(id)
    
    db.session.delete(soda)
    db.session.commit()
    
    response = soda_schema.dump(soda)
    return jsonify(response)