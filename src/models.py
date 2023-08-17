from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)             
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

class Character(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String(120), nullable=False)
    eye_color = db.Column(db.String(120), nullable=False)
    skin_color = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)

   

class Planet(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(120), nullable=False)
    terrain = db.Column(db.String(120), nullable=False)
    population = db.Column(db.Integer, nullable=False)

   

class Favorite(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # user = db.relationship(User)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    # planet = db.relationship(Planet)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    # character = db.relationship(Character)

# Estoy probando un push

    