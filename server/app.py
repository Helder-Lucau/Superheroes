#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, request
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

class HeroByID(Resource):
    # get the record using the id
    def get(self, id):

        hero = Hero.query.filter_by(id=id).first()
        if not hero:
            response_body = {"error": "Hero not found"}
            response = make_response(
                jsonify(response_body), 
                404
            )
            return response
        else:
            response_dict = hero.to_dict()
            response = make_response(
                jsonify(response_dict), 
                200
            )
            return response

# add the resource to the API   
api.add_resource(HeroByID, '/heroes/<int:id>')

class Powers(Resource):

    def get(self):
        power_dict = [p.to_dict() for p in Power.query.all()]

        response = make_response(
            jsonify(power_dict), 
            200
        )
        return response
    
# add the resource to the API   
api.add_resource(Powers, '/powers')

class PowerByID(Resource):
    def get(self, id):
        power = Power.query.filter_by(id=id).first()
        if not power:
            response_body = {"error": "Power not found"}
            response = make_response(
                jsonify(response_body),
                404
            )
        else:
            response_dict = power.to_dict()
            response = make_response(
                jsonify(response_dict), 
                200
            )
            return response
    
    def patch(self, id):

        power = Power.query.filter_by(id=id).first()
        if not power:
            return make_response({"error": "Power not found"}, 404)
        else:
            for attr in request.form:
                setattr(power, attr, request.form[attr])
            
            db.session.add(power)
            db.session.commit()
        
            response_dict = power.to_dict()
            response = make_response(
                jsonify(response_dict),
                200
            )
            return response
        
api.add_resource(PowerByID, '/powers/<int:id>')

# class HeroPowers(Resource):

#     def post(self):
#         try:
#             hero_data = request.get_json()
#             new_hero_power = HeroPower(
#                 strength=hero_data['strength'],
#                 hero_id=hero_data['hero_id'],
#                 power_id=hero_data['power_id'],
#         )
#             db.session.add(new_hero_power)
#             db.session.commit()
#             hero = Hero.query.filter(Hero.id==hero_data['hero_id']).first()
#             return hero, 201
#         except ValueError as e:
#             raise e

# # add the resource to the API
# api.add_resource(HeroPowers, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
