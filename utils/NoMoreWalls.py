# -*- coding: utf-8 -*-
import requests

from utils.proxyUtils import get_proxy


def get_content():
    proxies = get_proxy()
    url = 'https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.yml'
    print(url)
    file = requests.get(url, proxies=proxies)
    with open("pub/NoMoreWalls.yaml", "wb") as f:
        f.write(file.content)


if __name__ == '__main__':
    get_content()
