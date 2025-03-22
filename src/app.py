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
from models import db, User, Characters, Vehicles, Planets, Favourites
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

# Crear un nuevo usuario --> FUNCIONA
@app.route('/user', methods=['POST'])
def create_user():
    request_data = request.get_json()

    
    if not request_data.get('email') or not request_data.get('password') or not request_data.get('username') or not request_data.get('name') or not request_data.get('lastname'):
        return jsonify({"msg": "Email, password and username are required"}), 400

    
    existing_user = User.query.filter_by(email = request_data.get('email')).first()
    if existing_user:
        return jsonify({"msg": "User already exists"}), 403

    
    new_user = User(
        email = request_data["email"],
        password = request_data["password"],
        username = request_data["username"],
        name = request_data["name"],
        lastname = request_data["lastname"]
        
    )
 
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "msg" : "User created succesfully",
        "user" : new_user.serialize()
    }), 201


# Listar todos los registros de characters en la base de datos --> FUNCIONA
@app.route('/characters', methods=['GET'])
def get_all_characters():

    characters= Characters.query.all()
    characters_serialize = [character.serialize() for character in characters]

    if not characters:
        return jsonify({
            "msg": "Characters not found"
        }), 404
    
    return jsonify({
        "msg": "Characters retrieved successfully",
        "characters": characters_serialize 

    }),200

# Obtener un personaje por su id --> FUNCIONA
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):

    character= Characters.query.get(character_id)

    if not character:
        return jsonify({
            "msg": "Character not found"
        }), 404
    
    return jsonify({
        "msg": "Character found",
        "character": character.serialize()

    })

# Listar todos los registros de vehicles en la base de datos --> FUNCIONA
@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():

    vehicles= Vehicles.query.all()
    vehicles_serialize = [vehicle.serialize() for vehicle in vehicles]

    if not vehicles:
        return jsonify({
            "msg": "Vehicles not found"
        }), 404
    
    return jsonify({
        "msg": "Vehicles retrieved successfully",
        "vehicles": vehicles_serialize 

    }),200

# Obtener un vehiculo por su id --> FUNCIONA
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):

    vehicle= Vehicles.query.get(vehicle_id)

    if not vehicle:
        return jsonify({
            "msg": "Vehicle not found"
        }), 404
    
    return jsonify({
        "msg": "Vehicle found",
        "vehicle": vehicle.serialize()
    })

# Listar todos los registros de planetas en la base de datos --> FUNCIONA
@app.route('/planets', methods=['GET'])
def get_all_planets():

    planets= Planets.query.all()
    planets_serialize = [planet.serialize() for planet in planets]

    if not planets:
        return jsonify({
            "msg": "Planets not found"
        }), 404
    
    return jsonify({
        "msg": "Planets retrieved successfully",
        "planets": planets_serialize

    }),200

# Obtener un planeta por su id --> FUNCIONA
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    planet= Planets.query.get(planet_id)

    if not planet:
        return jsonify({
            "msg": "Planet not found"
        }), 404
    
    return jsonify({
        "msg": "Planet found",
        "planet": planet.serialize()

    }), 200


# Listar todos los usuarios del blog --> FUNCIONA
@app.route('/users', methods=['GET'])
def get_all_users():

    users = User.query.all()
    users_serialize =[user.serialize() for user in users]

    return  jsonify({
        "msg": "Users successfully retrieved",
        "users": users_serialize
    })


# Listar todos los favoritos que pertenecen al usuario actual --> FUNCIONA
@app.route('/<int:user_id>/favourites', methods=['GET'])
def get_user_favourites(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg":"User not found"}), 404

    return jsonify({
        "msg": "Favourites found succesfully",
        "favourites" : user.serialize_favourites()
    }), 200

# Añadir un nuevo planet favorito al usuario actual con el id = planet_id --> FUNCIONA
# Eliminar un planet favorito con el id = planet_id. --> FUNCIONA
@app.route('/favourite/planet/<int:planet_id>', methods=['POST', 'DELETE'])
def favourite_planet(planet_id):
    if request.method == 'POST': 
        request_data = request.get_json()
        
        if not request_data or not request_data.get("user_id"):
            return jsonify({"msg" : "Request incomplete"}), 400

        user = User.query.get(request_data.get("user_id"))
        planet = Planets.query.get(planet_id)
        planet_name=planet.serialize()["name"]

        
        if not user:
            return jsonify({"msg" : "User does not exist"}), 404
        

        new_favourite = Favourites(
            planet_id = planet_id,
            user_id = request_data.get("user_id")
        )
        
        db.session.add(new_favourite)
        db.session.commit()

        return jsonify({
            "msg" : planet_name + ' added successfully',
            "favourite" : new_favourite.serialize_all()
        }), 201    
    
    elif request.method == 'DELETE':
        request_data = request.get_json()
    
        if not request_data or not request_data.get("user_id"):
            return jsonify({"msg" : "Request incomplete"}), 400

        favourite = Favourites.query.filter_by(user_id=request_data.get("user_id"), planet_id=planet_id).first()

        if not favourite:
            return jsonify({"msg" : "Not found"}), 404
    
        db.session.delete(favourite)
        db.session.commit()

        return jsonify({"msg": "Favourite deleted successfully"}), 200


# Añade un nuevo character favorito al usuario actual con el id = character_id. --> FUNCIONA
# Elimina un character favorito con el id = character_id. --> FUNCIONA
@app.route('/favourite/character/<int:character_id>', methods=['POST','DELETE'])
def favourite_character(character_id):
    if request.method == 'POST':
        request_data = request.get_json()
    
        if not request_data or not request_data.get("user_id"):
            return jsonify({"msg" : "Request incomplete"}), 400

        user = User.query.get(request_data.get("user_id"))
        character = Characters.query.get(character_id)
        character_name= character.serialize()["name"]

    
        if not user:
            return jsonify({"msg" : "User does not exist"}), 404
    
    
        new_favourite = Favourites(
            character_id = character_id,
            user_id = request_data.get("user_id")
        )
    
        db.session.add(new_favourite)
        db.session.commit()

        return jsonify({
            "msg" : character_name + ' added successfully',
            "favourite" : new_favourite.serialize_all()
        }), 201   
    
    elif request.method == 'DELETE':

        request_data = request.get_json()
    
        if not request_data or not request_data.get("user_id"):
            return jsonify({"msg" : "Request incomplete"}), 400

        favourite = Favourites.query.filter_by(user_id=request_data.get("user_id"), character_id=character_id).first()

        if not favourite:
            return jsonify({"msg" : "Not found"}), 404

        db.session.delete(favourite)
        db.session.commit()

        return jsonify({"msg": "Favourite deleted successfully"}), 200

# Añade un nuevo vehicle favorito al usuario actual con el id = vehicle_id. --> FUNCIONA
# Elimina un vehicle favorito con el id = vehicle_id. --> FUNCIONA
@app.route('/favourite/vehicle/<int:vehicle_id>', methods=['POST', 'DELETE'])
def favourite_vehicle(vehicle_id):
    if request.method == 'POST':
        request_data = request.get_json()
    
        if not request_data or not request_data.get("user_id"):
            return jsonify({"msg" : "Request incomplete"}), 400

        user = User.query.get(request_data.get("user_id"))
        vehicle = Vehicles.query.get(vehicle_id)
        vehicle_name=vehicle.serialize()["name"]

    
        if not user:
            return jsonify({"msg" : "User does not exist"}), 404
    
    
        new_favourite = Favourites(
            vehicle_id = vehicle_id,
            user_id = request_data.get("user_id")
        )
    
        db.session.add(new_favourite)
        db.session.commit()

        return jsonify({
            "msg" : vehicle_name + ' added successfully',
            "favourite" : new_favourite.serialize_all()
        }), 201

    elif request.method == 'DELETE':
        request_data = request.get_json()
    
        if not request_data or not request_data.get("user_id"):
            return jsonify({"msg" : "Request incomplete"}), 400

        favourite = Favourites.query.filter_by(user_id=request_data.get("user_id"), vehicle_id=vehicle_id).first()

        if not favourite:
            return jsonify({"msg" : "Not found"}), 404

        db.session.delete(favourite)
        db.session.commit()

        return jsonify({"msg": "Favourite deleted successfully"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)