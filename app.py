from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def request_router():
    if request.method == "POST":
        # handle POST logic
        data = request.form.get("some_field")  # or request.json for JSON body
        return "Handled POST"
    else:
        # pass the verification
        return request.args.get("hub.challenge")
