import os
import json
from nexmo_jwt import JWTokenGenerator
import redis
import requests
import time
from pprint import pprint

from dotenv import load_dotenv
load_dotenv()

r = redis.Redis.from_url(os.getenv("REDIS_URL"))

gen = JWTokenGenerator(os.getenv('NEXMO_APP_ID'),os.getenv('PRIVATE_KEY_PATH'))

while True:
    message = r.lpop('queue:messages')
    if message:
        JWT = gen.generate_token()
        data = json.loads(message.decode('utf8'))

        if data["type"] == "whatsapp":
            # use the sandbox to send whatsapp
            api_url = os.getenv("SANDBOX_API_URL")

            msg = {'message': 
                    {'content':
                        {
                            'type':'text',
                            'text': data["message"]}},
                            'from': {'type': 'whatsapp', 'number': os.getenv("NEXMO_SANDBOX_NUMBER")},
                            'to': {'type': 'whatsapp', 'number': data["to"]}}

        else:
            # assume SMS, use live messages API
            api_url = os.getenv("MAIN_API_URL")

            msg = {'message': 
                    {'content':
                        {
                            'type':'text',
                            'text': data["message"]}},
                            'from': {'type': 'sms', 'number': os.getenv("NEXMO_NUMBER")},
                            'to': {'type': 'sms', 'number': data["to"]}}

        headers = {'Accept': 'application/json', 'Accept-Encoding':'identity', 'Authorization': 'Bearer ' + JWT.decode('utf8')}

        response = requests.post(api_url, json=msg, headers=headers)
        print(response.text)
        response_data = json.loads(response.text)
        if(response_data["message_uuid"]):
            r.set('messages:' + response_data["message_uuid"], 'attempted')

    time.sleep(0.1)


