# -*- coding: utf-8 -*-
import os
import traceback

import requests

from utils.formatUtils import write_yaml_file
from utils.proxyUtils import get_proxy


def get_content(current_work_dir):
    try:
        pub_dir = os.path.join(current_work_dir, 'pub')
        if not os.path.exists(pub_dir):
            os.makedirs(pub_dir)
        proxies = get_proxy()
        url = 'https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.yml'
        print(url)
        file = requests.get(url, proxies=proxies)
        yml_file_path = f"{pub_dir}/NoMoreWalls.yaml"
        write_yaml_file(file, yml_file_path)
    except Exception as e:
        print(traceback.format_exc())


if __name__ == '__main__':
    get_content("")
