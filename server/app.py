#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Hero, Power, HeroPower

# create your Flask Application and Set the DATABASE URI
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app) # connects our database to our application before it runs

api = Api(app)

@app.route('/')
def home():
    return '<h1>Welcome to Hero Power</h1>'

class Heroes(Resource):
    def get(self):
        hero_dict = [hr.to_dict() for hr in Hero.query.all()]
        response = make_response(jsonify(hero_dict), 200)
        return response
    
api.add_resource(Heroes, '/heroes')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
