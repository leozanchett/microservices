from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/super_simple', methods=['GET', 'POST'])
def super_simple():
    return jsonify(message='Hello from the Planetary API.'), 200

if __name__ == '__main__':
    app.run(debug=True)