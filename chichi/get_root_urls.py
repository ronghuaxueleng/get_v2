import json

import requests

from chichi.info import Info

root_url = "https://www.chichi-pui.com/api/posts/following/?age_limit=ALL"

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
    'referer': 'https://www.chichi-pui.com/posts/following/?age_limit=ALL&p=3',
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


if __name__ == '__main__':
    get_url(root_url)
