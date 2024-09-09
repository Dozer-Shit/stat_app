from flask import Flask, jsonify
import requests
import threading
import time

app = Flask(__name__)

site_status = {
    "status": "UNKNOWN",
    "code": None,
    "last_checked": None,
    "message": "No checks performed yet",
    "check_count": 0
}


def check_site_status(url):
    headers = {
        "User-Agent": "Chrome"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return {
                "status": "UP",
                "code": response.status_code,
                "message": f"Site {url} is reachable."
            }
        else:
            return {
                "status": "DOWN",
                "code": response.status_code,
                "message": f"Site {url} returned status code {response.status_code}."
            }
    except requests.exceptions.RequestException as e:
        return {
            "status": "ERROR",
            "code": None,
            "message": f"Error checking {url}: {e}"
        }


def periodic_check():
    site = "https://okulik.by"
    while True:
        global site_status
        result = check_site_status(site)
        site_status.update(result)
        site_status["last_checked"] = time.strftime("%Y-%m-%d %H:%M:%S")
        site_status["check_count"] += 1
        print(f"Checked site status: {site_status}")  # Вывод в консоль для отладки
        time.sleep(5)  # Ждём 5 секунд перед следующей проверкой


@app.route('/')
def index():
    return "Welcome to the status check application!"


@app.route('/status')
def status():
    return jsonify(site_status)


if __name__ == "__main__":
    # Запускаем фоновую задачу для периодической проверки статуса сайта
    checker_thread = threading.Thread(target=periodic_check)
    checker_thread.daemon = True  # Позволяет завершить поток при завершении основного приложения
    checker_thread.start()

    # Запускаем Flask-сервер
    app.run(host="0.0.0.0", port=8080)
