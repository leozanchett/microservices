import time

import redis, os
from flask import Flask


app = Flask(__name__)
cache = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count) 

@app.route('/health')
def health():
    return 'Not manssage\n'
