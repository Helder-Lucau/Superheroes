from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

# Initialize database
db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    serialize_rules = ('-hero_powers.hero',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now()) 

    # Relationship one to many 
    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')

class Power(db.Model, SerializerMixin):
    __tablename__='powers'

    serialize_rules = ('-hero_powers.power',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now()) 

    # Relationship one to many
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')

class HeroPower(db.Model, SerializerMixin):
    __tablename__='hero_powers'

    serialize_rules = ('-hero.hero_powers', '-power.hero_powers',)

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Relationship patterns many to one
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

