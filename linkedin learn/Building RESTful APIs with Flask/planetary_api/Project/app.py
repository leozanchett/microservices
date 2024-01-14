from flask import Flask, jsonify, request
import os
from models.base import db, ma

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'planets.db')

db.init_app(app) # initialize the database
ma.init_app(app) # initialize the marshmallow

from models.users import User
from models.planet import Planet

planets_schema = Planet.PlanetSchema(many=True)
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

if __name__ == '__main__':
    app.run(debug=True)


# cd 'C:\Users\lzandrade\Documents\GitHub\microservices\linkedin learn\Building RESTful APIs with Flask\planetary_api\Scripts'
# ./activate
# cd 'C:\Users\lzandrade\Documents\GitHub\microservices\linkedin learn\Building RESTful APIs with Flask\planetary_api\Project'
# python app.py