# Delivery Notification Sender

Put the messages you want to send on a queue and this tool will trickle out the messages at 10/sec and handle webhooks about message status updates. Useful as an addition to an existing API to regulate sending to avoid rate limits, and get status updates. Not useful as a standalone app ....

Message format ("sms" also supported as a message type):

```json
{
    "type": "whatsapp",
    "to": "447700900000",
    "message": "Your package has now been shipped! Please stand by to receive it"
}
```

Add messages to Redis with `RPUSH` to a list key.

## Set up the application

Copy `.env.example` to `.env` and complete/edit as needed.

Install dependencies with `pip install -r requirements.txt`

Run the worker (processes the queue and sends the messages to the Messages API): 

```
python worker.py
```

To get status updates of whether your messages have been submitted, delivered and (whatsapp only) read, run the webhook server:

```
python server.py
```

Use ngrok if developing locally, and update both your message sandbox URLs and the message URL settings of your application to point to `[ngrok URL]/webhooks/msg-status`.

Comments, issues and feedback are all welcome!

