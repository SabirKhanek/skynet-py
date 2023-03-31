from dotenv import load_dotenv
import os
if os.path.exists('./.env'):
    load_dotenv('./.env')
    print('environment loaded')
from flask import abort, current_app, make_response, request, Flask
from flask_cors import CORS
import json
from chatbot import generate_response
from datetime import datetime
from keygen import get_key, validate_key

app = Flask(__name__)
CORS(app)

# datetime object containing current date and time
now = datetime.now()

print(f"{__file__}: Server Started on: ", now)

app = Flask(__name__)
CORS(app)

pid = os.getpid()
print("PID: ", pid)
with open('server.pid', 'w') as f:
    f.write(str(pid))


@app.route("/api/gen_key", methods=["POST", "GET"])
def gen_key():
    req = request.get_json()
    print(req)
    if 'auth' not in req.keys():
        return make_response(json.dumps({"status": "error", "message": "No name found in the request"}), 400)
    elif req['auth'] != os.environ['admin_auth']:
        return make_response(json.dumps({"status": "error", "message": "Not allowed"}), 401)

    key_name = req['name'] if 'name' in req.keys() else "unspecified"

    resp = get_key({"name": key_name})

    re = {"status": "sky_success", "key": resp}
    print(f"Request: {req}\nResponse: {resp}")
    return make_response(json.dumps(re, indent=4), 200)


@app.route("/api/validate_key", methods=["GET", "POST"])
def validate_keygen_key():
    req = request.get_json()
    if 'key' not in req.keys():
        return make_response(json.dumps({"status": "error", "message": "No key found in the request"}), 400)
    isValid = validate_key(req['key'])
    re = {"status": "sky_success", "isValid": isValid}
    return make_response(json.dumps(re, indent=4), 200)


@app.route("/", methods=["GET"])
def index():
    re = {"status": "sky_success", "message": "Skynet Server is running"}

    return make_response(json.dumps(re, indent=4), 200)


@app.route("/api/generate_response", methods=["GET", "POST"])
def g_resp():
    req = request.get_json()
    if 'text' not in req.keys():
        return make_response(json.dumps({"status": "error", "message": "No text found in the request"}), 400)
    elif 'key' not in req.keys():
        return make_response(json.dumps({"status": "error", "message": "No key found in the request"}), 400)

    isValid = validate_key(req['key'])
    if not isValid:
        return make_response(json.dumps({"status": "error", "message": "Invalid key"}), 401)

    text = req['text']
    if not text:
        return make_response(json.dumps({"status": "error", "message": "Invalid text"}), 400)

    resp = generate_response(req['pastMessages'])

    re = {"status": "sky_success", "message": resp}
    print(f"Request: {text}\nResponse: {resp}")
    return make_response(json.dumps(re, indent=4), 200)


if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run(host='0.0.0.0', port='6929')
