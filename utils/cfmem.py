import os
import re
import traceback

import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery

from utils.formatUtils import write_yaml_file
from utils.proxyUtils import get_proxy


def get_content(current_work_dir):
    try:
        pub_dir = os.path.join(current_work_dir, 'pub')
        if not os.path.exists(pub_dir):
            os.makedirs(pub_dir)
        url = "https://www.cfmem.com/search/label/free"
        proxies = get_proxy()

        data = requests.get(url, proxies=proxies)
        text = data.text
        # print(text)
        soup = BeautifulSoup(text, "lxml")
        div_list = soup.findAll(
            name="a",
            attrs={"href": re.compile(r"https?://www\.cfmem\.com/\d{4}/\d{2}/\S+-v2rayclashsingbox-vpn.html")},
        )
        a_list = []
        p = re.compile(r"\d{4}年\d+月\d{2}(日)?\S*更新")
        for val in div_list[:1]:
            # print(val.text)
            if p.search(val.text):
                a_list.append(val.get("href"))

        new_v2ray_url = a_list[0]
        new_v2ray_data = requests.get(new_v2ray_url, proxies=proxies)
        new_v2ray_data_html = new_v2ray_data.text
        doc = PyQuery(new_v2ray_data_html)
        # print(new_v2ray_url)
        urls = re.findall(
            "clash -> https://fs.v2rayse.com/share/\d{8}/\S+.yaml", doc.text()
        )
        for url in urls:
            url = url.replace('clash -> ', '')
            print(url)
            file = requests.get(url, proxies=proxies, stream=True)
            yml_file_path = f"{pub_dir}/cfmem.yaml"
            write_yaml_file(file, yml_file_path)
    except Exception as e:
        print(traceback.format_exc())
        pass


if __name__ == '__main__':
    get_content()
