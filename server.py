from flask import Flask
from flask import request

import os
import json
import redis

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
r = redis.Redis.from_url(os.getenv("REDIS_URL"))


@app.route('/')
def entry_point():
    return 'OK'

@app.route('/webhooks/msg-event', methods=['POST'])
def status_update():
    data = request.get_json()

    r.set('messages:' + data['message_uuid'], data['status'])
    print("message " + data['message_uuid'] + ": " + data['status'], flush=True)

    return 'OK'

if __name__ == '__main__':
    app.run()
