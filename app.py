from flask import Flask, request
import requests
import os

FB_URL = "https://graph.facebook.com/v20.0"v  # /PAGE-ID/messages?access_token=YOUR_PAGE_ACCESS_TOKEN

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def request_router():
    if request.method == "POST":
        data = request.get_json()  # returns a dict (or None if parsing fails)
        print(data)
        return "Handled POST"
    else:
        # pass the verification
        return request.args.get("hub.challenge")
