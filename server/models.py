from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize database
db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    serialize_rules = ('-heropowers.hero.heropowers',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now()) 

    # creating a one to many association betweem Hero and HeroPower 
    heropowers = db.relationship('HeroPower', backref='heroes')

    # Instance method that determines the standard output value
    def __repr__(self):
        return f'Hero name:{self.name}, Super name: {self.super_name}'

class Power(db.Model, SerializerMixin):
    __tablename__='powers'

    serialize_rules = ('-heropowers.power.heropowers',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now()) 

    # creating a one to many association betweem power and HeroPower 
    heropowers = db.relationship('HeroPower', backref='powers')

    # Validate description must be at least 20 characters long
    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return description

    # Instance method that returns a printable representation of the object
    def __repr__(self):
        return f'Power name:{self.name}, Description: {self.description}'
    
class HeroPower(db.Model, SerializerMixin):
    __tablename__='hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # validation: strength must be one of the following values ['Strong', 'Weak', 'Average']
    @validates("strength")
    def validate_strength(self, key, strength):
        strengths = ['Strong', 'Weak', 'Average']
        if not strength in strengths:
            raise ValueError("Strength must be one of the following values: 'Strong', 'Weak', 'Average'")
        return strength
    
    # Instance method that returns a printable representation of the object
    def __repr__(self):
        return f'Strength:{self.strength}, Hero:{self.hero_id}, Power:{self.power_id}'