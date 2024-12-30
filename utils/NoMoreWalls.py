# -*- coding: utf-8 -*-
import os

import requests

from utils.proxyUtils import get_proxy


def get_content(current_work_dir):
    pub_dir = os.path.join(current_work_dir, 'pub')
    if not os.path.exists(pub_dir):
        os.makedirs(pub_dir)
    proxies = get_proxy()
    url = 'https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.yml'
    print(url)
    file = requests.get(url, proxies=proxies)
    yml_file_path = f"{pub_dir}/NoMoreWalls.yaml"
    with open(yml_file_path, "wb") as f:
        f.write(file.content)


if __name__ == '__main__':
    get_content()
