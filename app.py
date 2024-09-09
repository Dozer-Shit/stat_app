from flask import Flask, jsonify
import requests

app = Flask(__name__)


def check_site_status(url):
    headers = {
        "User-Agent": "Chrome"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return {"status": "UP", "code": response.status_code}
        else:
            return {"status": "DOWN", "code": response.status_code}
    except requests.exceptions.RequestException as e:
        return {"status": "ERROR", "message": str(e)}


@app.route('/')
def index():
    return "Welcome to the status check application!"


@app.route('/status')
def status():
    site = "https://okulik.by"
    result = check_site_status(site)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
