import time
import requests


def check_site_status(url):
    headers = {
        "User-Agent": "Chrome"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"Site {url} is UP!")
        else:
            print(f"Site {url} returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error checking {url}: {e}")


if __name__ == "__main__":
    site = "https://okulik.by"
    while True:
        check_site_status(site)
        time.sleep(10)
