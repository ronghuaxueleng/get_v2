import re
import base64
import urllib

import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery
from ruamel import yaml

from utils.formatUtils import reset_yaml_stream


def get_content():
    url = 'aHR0cHM6Ly9jbGFzaGZhbi5jb20vZnJlZW5vZGUv'
    url = base64.b64decode(url).decode("utf-8")

    data = requests.get(url)
    text = data.text
    try:
        doc = PyQuery(text)
        urls = re.findall(
            "https?://www\.qilin2\.com\/api\/v1\/client\/subscribe\?token=\S{32}", doc.text()
        )
        for url in urls:
            url = f"http://sub.id9.cc/sub?target=clash&new_name=true&url={urllib.parse.quote(url, safe='')}&insert=false&config=https%3A%2F%2Fraw.githubusercontent.com%2FACL4SSR%2FACL4SSR%2Fmaster%2FClash%2Fconfig%2FACL4SSR_Online.ini"
            file = requests.get(url, stream=True)
            yml = yaml.YAML()
            yml.indent(mapping=2, sequence=4, offset=2)
            with open("pub/qilin.yaml", "w+", encoding="utf8") as outfile:
                yml.dump(reset_yaml_stream(file.content), outfile)
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    get_content()