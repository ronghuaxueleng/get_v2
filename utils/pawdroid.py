import os
import re
import shutil

import requests

from utils.proxyUtils import get_proxy
from utils.yamlUtils import YamlUtils


def get_content():
    proxies = get_proxy()

    pawdroid = os.path.join("pawdroid")
    yamlUtils = YamlUtils(pawdroid)
    yamlUtils.clone_repo("https://github.com/Pawdroid/Free-servers.git")
    with open(os.path.join(pawdroid, "README.md"), "r", encoding='utf-8') as f:
        content = f.read()
        urls = re.findall(r"https://shadowshare.v2cross.com/publicserver/servers/temp/\w+", content)
        if len(urls) > 0:
            url = urls[0]
            url = "https://api.dler.io/sub?target=clash&new_name=true&url={}&insert=false&config=https://raw.fastgit.org/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online.ini".format(url)
            file = requests.get(url, proxies=proxies)
            with open("pub/pawdroid.yaml", "wb") as f:
                f.write(file.content)
    shutil.rmtree(pawdroid)


if __name__ == '__main__':
    get_content()
