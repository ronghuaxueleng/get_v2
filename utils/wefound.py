import re

import requests
from ruamel import yaml

from utils.formatUtils import reset_yaml_stream
from utils.proxyUtils import get_proxy


def get_content():
    url = "https://wefound.cc/p/53"
    proxies = get_proxy()

    data = requests.get(url, proxies=proxies)
    text = data.text
    try:
        urls = re.findall(r"https?://wefound.cc/freenode/\d{4}/\d{2}/\d{8}\.yaml", text)
        print(urls)
        file = requests.get(urls[0], proxies=proxies, stream=True)
        yml = yaml.YAML()
        yml.indent(mapping=2, sequence=4, offset=2)
        with open("pub/wefound.yaml", "w+", encoding="utf8") as outfile:
            yml.dump(reset_yaml_stream(file.content), outfile)
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    get_content()
