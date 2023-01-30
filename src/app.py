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
from models import db, User, People, Planets, Vehicles, Likes
#from models import Person
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

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

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Creo el registro del usuario

@app.route("/signup", methods=["POST"])
def signup():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user_signup= User.query.filter_by(email=email).first()

    if email != user_signup.email or password != user_signup.password:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

    # Inicio de sesión

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user_login= User.query.filter_by(email=email).first()

    if email != user_login.email or password != user_login.password:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

    # Validación

@app.route("/private", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    
    current_user = get_jwt_identity()
    user_private= User.query.filter_by(email=current_user).first()
    return jsonify(logged_in_as=user_private.serialize()), 200


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
    
    # Rutas

    # GET 1

@app.route('/people', methods=['GET'])
def hello_people():
    all_people=People.query.all()
    results = list(map(lambda item: item.serialize(), all_people))
    
    return jsonify(results), 200

    # GET 2

@app.route('/people/<int:people_id>', methods=['GET'])
def hello_one_people(people_id):
    one_people=People.query.filter_by(id=people_id).first()
 
    return jsonify(one_people.serialize()), 200

    # GET 3


@app.route('/planets', methods=['GET'])
def hello_planets():
    all_planets=Planets.query.all()
    results = list(map(lambda item: item.serialize(), all_planets))
    
    return jsonify(results), 200

    # GET 4

@app.route('/planets/<int:planets_id>', methods=['GET'])
def hello_one_planet(planets_id):
    one_planet=Planets.query.filter_by(id=planets_id).first()

    return jsonify(one_planet.serialize()), 200

    # GET 5

@app.route('/user', methods=['GET'])
def hello_user():
    all_user=User.query.all()
    results = list(map(lambda item: item.serialize(), all_user))
    
    return jsonify(results), 200

    # GET 6

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def hello_user_likes(user_id):
    user_likes=Likes.query.filter_by(user_id=user_id).all()
    results = list(map(lambda item: item.serialize(), user_likes))

    return jsonify(results), 200

    # POST 1

@app.route('/user/<int:user_id>/favorites/planet', methods=['POST'])
def add_favoriteplanet (user_id):

    request_body=request.json

    # print(request_body)

    # print(request_body['planets_id'])

    # return jsonify(request_body)

    my_fav= Likes(user_id=user_id, people_id= None, vehicles_id= None, planets_id= request_body['planets_id']) 

    the_favs = Likes.query.filter_by(user_id=user_id, planets_id= request_body['planets_id']).first()

    print(the_favs)

    if the_favs is None:

        my_fav= Likes(user_id=user_id, people_id= None, vehicles_id= None, planets_id= request_body['planets_id']) 

        db.session.add(my_fav)
        db.session.commit()

        return jsonify({"msg": "Su favorito ha sido agregado"}), 200

    return jsonify({"msg": "El favorito no existe"}), 400

    # POST 2

@app.route('/user/<int:user_id>/favorites/people', methods=['POST'])
def add_favoritepeople (user_id):

    request_body=request.json

    # print(request_body)

    # print(request_body['planets_id'])

    # return jsonify(request_body)

    my_person= Likes(user_id=user_id, vehicles_id= None, planets_id= None, people_id=request_body['people_id']) 

    the_favs_people = Likes.query.filter_by(user_id=user_id, people_id=request_body['people_id']).first()

    print(the_favs_people)

    if the_favs_people is None:

        my_person= Likes(user_id=user_id, vehicles_id= None, planets_id= None, people_id=request_body['people_id']) 

        db.session.add(my_person)
        db.session.commit()

        return jsonify({"msg": "Su favorito ha sido agregado"}), 200

    return jsonify({"msg": "El favorito no existe"}), 400

    # DELETE 1

@app.route('/user/<int:user_id>/favorites/planet', methods=['DELETE'])
def delete_favoriteplanet (user_id):

    request_body=request.json

    # print(request_body)

    # print(request_body['planets_id'])

    # return jsonify(request_body)

    # delete_my_fav= Likes(user_id=user_id, people_id= None, vehicles_id= None, planets_id= request_body['planets_id']) 

    favs_to_delete = Likes.query.filter_by(user_id=user_id, planets_id= request_body['planets_id']).first()

    print(favs_to_delete)

    if favs_to_delete is not None:

        # delete_my_fav= Likes(user_id=user_id, people_id= None, vehicles_id= None, planets_id= request_body['planets_id']) 

        db.session.delete(favs_to_delete)
        db.session.commit()

        return jsonify({"msg": "Su planeta favorito ha sido eliminado"}), 200

    return jsonify({"msg": "El favorito que deseas eliminar no existe"}), 400

# DELETE 2

@app.route('/user/<int:user_id>/favorites/people', methods=['DELETE'])
def delete_favoritepeople (user_id):

    request_body=request.json

    # print(request_body)

    # print(request_body['planets_id'])

    # return jsonify(request_body)

    delete_favs_people = Likes.query.filter_by(user_id=user_id, people_id= request_body['people_id']).first()

    print(delete_favs_people)

    if delete_favs_people is not None:

        db.session.delete(delete_favs_people)
        db.session.commit()

        return jsonify({"msg": "Su personaje favorito ha sido eliminado"}), 200

    return jsonify({"msg": "El favorito que deseas eliminar no existe"}), 400





        









    
    # Ejemplo

# @app.route('/user', methods=['GET'])
# def handle_hello():

    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }

    # return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


