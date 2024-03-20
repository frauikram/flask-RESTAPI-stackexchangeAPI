from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.config['ENV'] = 'development'
app.config['FLASK_DEBUG'] = True

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = True
# app.config['JSONIFY_MIMETYPE'] = 'application/json'


db = SQLAlchemy(app)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(120))
    
    def __repr__(self) :
        return f"{self.name} - {self.description}"
    
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return 'Hello!'

@app.route('/drinks')
def get_drinks():    
    drinks = Drink.query.all()
    output = []
    for drink in drinks:
        drink_data = {"id": drink.id,"name": drink.name, "description": drink.description}
        output.append(drink_data)
    # return jsonify({"drinks": output})
    return {"drinks": output}

@app.route('/drinks/<id>')
def get_drink(id):    
    drink = Drink.query.get_or_404(id)
    drink_data = {"name": drink.name, "description": drink.description}
    return jsonify(drink_data)
    # return drink_data
    

@app.route('/drinks', methods=['POST'])
def add_drink():    
    drink = Drink(name=request.json['name'], description= request.json['description'])
    db.session.add(drink)
    db.session.commit()
    # return jsonify({"drinks": output})
    return {"id": drink.id}

@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):  
    drink = Drink.query.get(id)
    if drink is None:
        return {"error: drink {drink} not found"}
    db.session.delete(drink)
    db.session.commit()
    return {"deleted drink id": id}

# @app.route('/drinks/<d_id>', methods=['PUT'])
# def add_drink_id(d_id):    
#     drink = Drink(id= d_id, name=request.json['name'], description= request.json['description'])
#     db.session.add(drink)
#     db.session.commit()
#     # return jsonify({"drinks": output})
#     return {"id": drink.d_id}

# used POSTMAN.io to check api endpoints for post and delete