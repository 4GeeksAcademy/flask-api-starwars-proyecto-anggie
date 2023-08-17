"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap 
from admin import setup_admin
from models import db, User , Character , Planet , Favorite
from flask_sqlalchemy import SQLAlchemy
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def list_users():
    user = User.query.all()
    users_list = list(map(lambda x : x.to_dict(), user))
    return jsonify(users_list)


@app.route('/people', methods=['GET'])
def list_people():
    people = Character.query.all()
    people_list = list(map(lambda x : x.to_dict(), people))
    return jsonify(people_list)

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Character.query.get(people_id)
    return jsonify(person.to_dict())


@app.route('/planets', methods=['GET'])
def list_planet():
    planet = Planet.query.all()
    planet_list = list(map(lambda x : x.to_dict(), planet))
    return jsonify(planet_list)

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    return jsonify(planet.to_dict())

@app.route('/favorites/character/<int:character_id>/<int:user_id>', methods=['POST'])
def add_favorite_character(character_id, user_id):
    favorite_character = Favorite(user_id = user_id, character_id = character_id)
    db.session.add(favorite_character)
    db.session.commit()
    respuesta = {"mensaje" : "El personaje fue añadido a la lista de favoritos"}
    return jsonify(respuesta)


@app.route('/favorites/character/<int:character_id>/<int:user_id>', methods=['DELETE'])
def delete_favorite_character(character_id, user_id):
    
    favorite_character = db.session.execute(
            db.select(Favorite)
            .filter(Favorite.user_id == user_id, Favorite.character_id == character_id)
        ).scalar()
    if favorite_character is None:
        return jsonify({"mensaje" : "El personaje no esta en la lista de favoritos"}), 404
    db.session.delete(favorite_character)
    db.session.commit()
    
    respuesta = {"mensaje" : "El personaje fue ELIMINADO"}
    print(favorite_character)
    return jsonify(respuesta)


@app.route('/favorites/planets/<int:planet_id>/<int:user_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id, user_id):
    favorite_planet = db.session.execute(
            db.select(Favorite)
            .filter(Favorite.user_id == user_id, Favorite.planet_id == planet_id)
        ).scalar()
    if favorite_planet is None:
        return jsonify({"mensaje" : "El planeta no esta en la lista de favoritos"}), 404
    db.session.delete(favorite_planet)
    db.session.commit()
    
    respuesta = {"mensaje" : "El planeta fue ELIMINADO"}
    print(favorite_planet)
    return jsonify(respuesta)


@app.route('/favorites/planets/<int:planet_id>/<int:user_id>', methods=['POST'])
def add_favorite_planet(planet_id, user_id):
    favorite_planet = Favorite(user_id = user_id, planet_id = planet_id)
    db.session.add(favorite_planet)
    db.session.commit()
    respuesta = {"mensaje" : "El planeta fue añadido a la lista de favoritos"}
    return jsonify(respuesta)

@app.route('/favorites', methods=['GET'])
def get_all_favorites():
    all_favorites= Favorite.query.all()
    favorites_list = list(map(lambda x: x.to_dict(), all_favorites))
    return jsonify(favorites_list), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
