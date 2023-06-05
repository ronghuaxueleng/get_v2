import requests


def get_proxy():
    proxies = {}
    try:
        requests.get("http://localhost:1080")
        proxies = {
            "http": "http://localhost:1080",
            "https": "http://localhost:1080",
        }
    except Exception as e:
        pass
    return proxies