from flask import Flask, jsonify, request
import os
from models.base import db, ma
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message
from decouple import config
from datetime import timedelta
import jwt as jwt_lib

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'planets.db')
app.config['JWT_SECRET_KEY'] = 'super-secret' # change this IRL

app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = config('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = config('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db.init_app(app) # initialize the database
ma.init_app(app) # initialize the marshmallow
jwt = JWTManager(app) # initialize the jwt manager
mail = Mail(app) # initialize the mail extension

from models.users import User
from models.planet import Planet

planets_schema = Planet.PlanetSchema(many=True)
planet_schema = Planet.PlanetSchema()
users_schema = User.UserSchema(many=True)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')

@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name='Mercury',
                    planet_type='Class D',
                    home_star='Sol',
                    mass=3.258e23,
                    radius=1516,
                    distance=35.98e6)
    venus = Planet(planet_name='Venus',
                    planet_type='Class K',
                    home_star='Sol',
                    mass=4.867e24,
                    radius=3760,
                    distance=67.24e6)
    earth = Planet(planet_name='Earth',
                    planet_type='Class M',
                    home_star='Sol',
                    mass=5.972e24,
                    radius=3959,
                    distance=92.96e6)
    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(first_name='William',
                    last_name='Herschel',
                    email='teste@gmail.com',
                    password='password')
    db.session.add(test_user)
    db.session.commit()
    print('Database seeded!')

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/super_simple', methods=['GET', 'POST'])
def super_simple():
    return jsonify(message='Hello from the Planetary API 3.'), 200

@app.route('/not_found')
def not_found():
    return jsonify(message='That resource was not found'), 404

@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    print(request.args)
    if age < 18:
        return jsonify(message='Sorry ' + name + ', you are not old enough'), 401
    else:
        return jsonify(message='Welcome ' + name + ', you are old enough')

@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message='Sorry ' + name + ', you are not old enough'), 401
    else:
        return jsonify(message='Welcome ' + name + ', you are old enough')

@app.route('/planets', methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(result)

@app.route('/users', methods=['GET'])
def users():
    users_list = User.query.all()
    result = users_schema.dump(users_list)
    return jsonify(result)

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    print(test)
    if test:
        return jsonify(message='That email already exists'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']

        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User created successfully'), 201
    
@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']
    
    test = User.query.filter_by(email=email, password=password).first()
    if test:
        expires = timedelta(minutes=15)
        access_token = create_access_token(identity=email, expires_delta=expires)
        return jsonify(message='Login succeeded!', access_token=access_token)
    else:
        return jsonify(message='Bad email or password'), 401
    
@app.route('/retrieve_password/<string:email>', methods=['GET'])
@jwt_required()
def retrieve_password(email: str):
    user = User.query.filter_by(email=email).first()
    if user:
        msg = Message('your planetary API password is ' + user.password,
                      sender = 'admin@planetary-api.com',
                      recipients=[email])
        mail.send(msg)
        return jsonify(message='Password sent to ' + email)
    else:
        return jsonify(message='That email does not exist'), 401
    

@app.route('/verify_token_expire', methods=['GET'])
@jwt_required()
def verify_token_expire():
    auth = request.headers['Authorization'].split(' ')[1]
    payload =  jwt_lib.decode(jwt=auth, algorithms=['HS256'], key='super-secret')
    return jsonify(message='Token is valid', payload=payload, exp=payload['exp'])


@app.route('/planet_details/<int:planet_id>', methods=['GET'])
@jwt_required()
def planet_details(planet_id: int):
    print("Planet ID: ", planet_id)
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        result = planet_schema.dump(planet)
        print("Result: ", result)
        return jsonify(result)
    else:
        return jsonify(message='That planet does not exist'), 404
    
@app.route('/add_planet', methods=['POST'])
@jwt_required()
def add_planet():
    planet_name = request.form['planet_name']
    test = Planet.query.filter_by(planet_name=planet_name).first()
    if test:
        return jsonify(message='There is already a planet by that name'), 409
    else:
        planet_type = request.form['planet_type']
        home_star = request.form['home_star']
        mass = float(request.form['mass'])
        radius = float(request.form['radius'])
        distance = float(request.form['distance'])
        
        new_planet = Planet(planet_name=planet_name, planet_type=planet_type, home_star=home_star, mass=mass, radius=radius, distance=distance)
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(message='You added a planet'), 201
                
if __name__ == '__main__':
    print('Starting API')
    app.run(debug=True)


# cd 'C:\Users\lzandrade\Documents\GitHub\microservices\linkedin learn\Building RESTful APIs with Flask\planetary_api\Scripts'
# ./activate
# cd 'C:\Users\lzandrade\Documents\GitHub\microservices\linkedin learn\Building RESTful APIs with Flask\planetary_api\Project'
# python app.py