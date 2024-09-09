from flask import Flask, jsonify
import requests
import threading
import time

app = Flask(__name__)

site_status = {"status": "UNKNOWN", "code": None}


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


def periodic_check():
    site = "https://okulik.by"
    while True:
        global site_status
        site_status = check_site_status(site)
        print(f"Checked site status: {site_status}")  # Это выводится в консоль для отладки
        time.sleep(5)


@app.route('/')
def index():
    return "Welcome to the status check application!"


@app.route('/status')
def status():
    return jsonify(site_status)


if __name__ == "__main__":
    checker_thread = threading.Thread(target=periodic_check)
    checker_thread.daemon = True
    checker_thread.start()

    app.run(host="0.0.0.0", port=8080)
