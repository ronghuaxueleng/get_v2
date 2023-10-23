import json
import os
import urllib
from multiprocessing import cpu_count, Pool

import requests
from bs4 import BeautifulSoup

from chichi.info import Info, Image

domain = "https://www.chichi-pui.com"
root_url = f"{domain}/api/posts/following/?age_limit=ALL"

payload = {}
headers = {
    'authority': 'www.chichi-pui.com',
    'sec-ch-ua': '"Chromium";v="21", " Not;A Brand";v="99"',
    'accept': 'application/json, text/plain, */*',
    'dnt': '1',
    'x-csrftoken': 'n2XvDIiH4lWWFh9K1OJZLqSA34fCxnvp',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.chichi-pui.com',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'GMORW_UID=121740c4b3a2541727fcd68a910298dcdc; GMOSSP_USER=RhF8gLmB8VlhSwhE; _ga=GA1.1.266257206.1689174092; cto_bundle=Q_1sc190TDVrR2ZaOTdQbDBSJTJCaFdlUVM2N1R4VG4yNyUyQllSZjdudFdzZWJuJTJCJTJGVGxBUUJvMTN2d3BtN0RPV0twd1FvOG5Ic1ZybVIzUnFTaXY0WWNSRE5vSG45RDR4ZTFCdW1SNXhOOVMyJTJCVEI2RiUyRmFZWkh2eFFSRlp4S2VBNGJETFBNd1ExV0lFYUxaRWFwS2ZHZSUyRjJ2QTA2USUzRCUzRA; _ga_4WN5YTWQFK=GS1.1.1689254106.2.1.1689256076.0.0.0; csrftoken=aM1r7YVBR7W8H8vNwGdhEfhD9MnO0r0U; csrf_cookie=n2XvDIiH4lWWFh9K1OJZLqSA34fCxnvp; session_cookie=9i6e6tm3o25mc9qozng7r37vhak5apdi'
}


def get_url(url):
    print('url is :' + url)
    response = requests.request("GET", url, headers=headers, data=payload)
    html = response.text
    res_json = json.loads(html)
    next_url = res_json.get('next')
    results = res_json.get('results')
    if results is not None:
        for result in results:
            try:
                data = {}
                data['postId'] = result.get('id')
                data['userName'] = result['user']['display_name']
                data['url'] = result.get('url')
                data['imagesCount'] = result.get('images_count')
                Info.insert(data).execute()
            except Exception as e:
                print(e)
                pass
    try:
        get_url(next_url)
    except Exception as e:
        print(e)


def save_image_url():
    posts = Info.select().where(Info.grabState != 1).execute()
    if len(posts) > 0:
        for post in posts:
            try:
                url = f"{domain}{post.url}"
                response = requests.request("GET", url, headers=headers, data=payload)
                text = response.text
                soup = BeautifulSoup(text, "lxml")
                image_link_container = soup.select('.js-main-image-link')
                print(f"页面【{url}】")
                print(f"获取{len(image_link_container)}张图片")
                for image_link in image_link_container:
                    try:
                        image_data = {}
                        image_data['root_url'] = url
                        image_data['image_url'] = image_link.get("href")
                        Image.insert(image_data).execute()
                    except Exception as e:
                        print(e)
                Info.update(grabState=1).where(Info.postId == post.postId).execute()
            except Exception as e:
                print(e)


def request_image(url, image_name, PROXIES=None):
    print(("正在下载 %s" % image_name))
    try:
        os.makedirs("images", exist_ok=True)
        req = urllib.request.Request(url)
        req.add_header('User-Agent', headers['user-agent'])
        req.add_header('Cache-Control', 'no-cache')
        req.add_header('Accept', '*/*')
        req.add_header('Accept-Encoding', 'gzip, deflate')
        req.add_header('Connection', 'Keep-Alive')

        if PROXIES is not None:
            opener = urllib.request.build_opener(urllib.request.ProxyHandler(PROXIES))
            urllib.request.install_opener(opener)

        resp = urllib.request.urlopen(req)

        respHtml = resp.read()
        path = 'images/%s' % image_name

        binfile = open(path, "wb")
        binfile.write(respHtml)

        binfile.close()
        Image.update(grabState=1).where(Image.image_url == url).execute()
        print(("%s 下载成功" % image_name))
        return True
    except Exception as e:
        print(e)
        print(("%s 下载失败" % image_name))
        return False


def download_image(proxy=None):
    images = Image.select().where(Image.grabState != 1).execute()
    if len(images) > 0:
        cpu_counts = cpu_count()
        print("cup数量：{}".format(cpu_counts))
        pool = Pool(processes=cpu_counts)
        for img in images:
            request_image(img.image_url, img.id + ".png", PROXIES=proxy)
        pool.close()
        pool.join()  # 运行完所有子进程才能顺序运行后续程序


if __name__ == '__main__':
    save_image_url()
