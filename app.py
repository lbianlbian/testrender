from flask import Flask, request
import requests
import os

FB_URL = "https://graph.facebook.com/v20.0"  # /PAGE-ID/messages?access_token=YOUR_PAGE_ACCESS_TOKEN
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def request_router():
    if request.method == "POST":
        ''' message payload structure
        {
          "sender": {
            "id": "<PSID>"
          },
          "recipient": {
            "id": "<PAGE_ID>"
          },
          "timestamp": 1458692752478,
          "message": {
            "mid": "mid.1457764197618:41d102a3e1ae206a38",
            "text": "hello, world!"
          }
        }
        '''
        incoming_payload = request.get_json()
        data = incoming_payload["entry"][0]["messaging"][0]
        page_id = data["recipient"]["id"]
        payload = {
            "recipient": { "id": data["sender"]["id"] },
            "messaging_type": "RESPONSE",
            "message": { "text": f"Hey! Here's your answer. {data['message']['text']}" }
        }
        requests.post(f"{FB_URL}/{page_id}/messages?access_token={PAGE_ACCESS_TOKEN}", json=payload)
        return "Handled POST"
    else:
        # pass the verification
        return request.args.get("hub.challenge")
