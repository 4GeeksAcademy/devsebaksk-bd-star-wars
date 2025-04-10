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
from models import db, User, People, Planets, Favorites
import random
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



@app.route('/users', methods=['GET'])
def handle_users():
    try:
        users_list = []
        users = db.session.execute(db.select(User)).scalars().all()
        for u in users:
            users_list.append(u.serialize())
        return jsonify(users_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@app.route('/favorite', methods=['GET'])
def handle_users_favorites():
    try:
        users_favorites_planets_list = []
        users_favorites_planets = db.session.execute(db.select(Favorites)).scalars().all()
        for u in users_favorites_planets:
            users_favorites_planets_list.append(u.serialize())
        return jsonify(users_favorites_planets_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(silent=True)

    if not data or "username" not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        user = User(username=data["username"],
                    firstname=data["firstname"],
                    lastname=data["lastname"],
                    email=data["email"]
                    )
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500





@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def create_fav_planet(planet_id):
    data = request.get_json(silent=True)

    if not data or "user_id" not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        fav_planet = Favorites(user_id=data["user_id"],
                    planet_id=planet_id
                    )
        db.session.add(fav_planet)
        db.session.commit()
        return jsonify(fav_planet.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def create_fav_people(people_id):
    data = request.get_json(silent=True)

    if not data or "user_id" not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        fav_people = Favorites(user_id=data["user_id"],
                    people_id=people_id
                    )
        db.session.add(fav_people)
        db.session.commit()
        return jsonify(fav_people.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500





@app.route('/people', methods=['GET'])
def handle_people():
    try:
        people_list = []
        people = db.session.execute(db.select(People)).scalars().all()
        for p in people:
            people_list.append(p.serialize())
        return jsonify(people_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/people/<int:people_id>', methods=['GET'])
def handle_people_id(people_id):
    try:
        people_list = []
        people = db.session.execute(db.select(People)).scalars().all()
        for p in people:
            people_list.append(p.serialize())
        miembro = list(filter(lambda x: x['id'] == people_id, people_list))
        return jsonify(miembro)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planet_id(planet_id):
    try:
        planets_list = []
        planets = db.session.execute(db.select(Planets)).scalars().all()
        for p in planets:
            planets_list.append(p.serialize())
        planet = list(filter(lambda x: x['id'] == planet_id, planets_list))
        return jsonify(planet)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/planets', methods=['GET'])
def handle_planets():
    try:
        planet_list = []
        planet = db.session.execute(db.select(Planets)).scalars().all()
        for p in planet:
            planet_list.append(p.serialize())

        return jsonify(planet_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/favorite/<int:fav_id>", methods=["DELETE"])
def delete_user(fav_id):
    fav = db.get_or_404(Favorites, fav_id)

    try:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({"message": "Usuario eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
