import requests

from utils.proxyUtils import get_proxy


def get_content():
    proxies = get_proxy()
    url = 'https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub'
    url = "https://url.v1.mk/sub?target=clash&new_name=true&url={}&insert=false&config=https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online.ini".format(url)
    print(url)
    file = requests.get(url, proxies=proxies)
    with open("pub/pawdroid.yaml", "wb") as f:
        f.write(file.content)


if __name__ == '__main__':
    get_content()
