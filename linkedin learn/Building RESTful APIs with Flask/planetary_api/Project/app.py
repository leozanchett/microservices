from flask import Flask, jsonify, request


app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)