from flask import Flask, request
import requests
import os

FB_URL = "https://graph.facebook.com/v20.0"  # /PAGE-ID/messages?access_token=YOUR_PAGE_ACCESS_TOKEN
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_HEADERS = {
    "Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}"
}
    
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
            "message": { "text": call_llm(data["message"]["text"]) }
        }
        requests.post(f"{FB_URL}/{page_id}/messages?access_token={PAGE_ACCESS_TOKEN}", json=payload)
        return "Handled POST"
    else:
        # pass the verification
        return request.args.get("hub.challenge", "default get request value returned")

PROMPT = '''You are a rug pricing assistant for The Rug Finder. A designer will describe 
spec changes to a base rug. Your job:

1. Identify which specs they're changing (size, KPSI, color)
2. Calculate the price impact for each change using the pricing table below
3. Show an itemized breakdown, then the new total
4. If a request falls outside these specs (custom shapes, materials, rush 
   timelines, etc.), say this needs to go to the vendor directly rather 
   than guessing

Base rug: 9'x12', wool, 100 KPSI, undyed = $900
Pricing rules:
- Size: +$18 per sq ft above 40 sq ft (5x8 base)
- Knot density: +$60 per +25 KPSI above 100
- Color: red +$50, blue +$120, green +$180, undyed +$0

Always show your itemized math before the total. No markdown, lists, bullet points. Plain text only because this is going in a Facebook Messenger message.'''

def call_llm(query):
    payload = {
        "model": "mistral-medium-latest",
        "messages": [
            {
                "role": "system",
                "content": PROMPT
            },
            {
                "role": "user",
                "content": query
            }
        ]
    }
    resp_raw = requests.post(MISTRAL_URL, headers=MISTRAL_HEADERS, json=payload)
    resp = resp_raw.json()
    return resp["choices"][0]["message"]["content"][0]["text"]
