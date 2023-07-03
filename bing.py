import requests
import json
from bs4 import BeautifulSoup
from googletrans import Translator

# url = 'https://cn.bing.com/ttranslate?&category=&IG=C4A52C35D175427988E6510779DEFB5F&IID=translator.5036.8'
url = 'https://www.bing.com/translator?ref=TThis&text=&from=en&to=zh-Hans'


def translate_weiruan(info, fr='zh-CHS', to="en"):
    tran = Translator(service_urls=['translate.google.cn'])
    res = tran.translate(info, dest='ca')
    print(res)
    # res = requests.post(url, data={'text': info, 'from': fr, 'to': to, 'doctype': 'json'})
    # res.raise_for_status()
    # print(BeautifulSoup(res.text, 'html.parser'))

    exit()
    return res.json()['translationResponse']


def is_Chinese(str):  # 判断输入的内容是否是中文
    for ch in str:
        if '\u4e00' <= ch <= '\u9fff':
            return True
        else:
            return False


def start_translate(trans):
    if is_Chinese(trans):  # 实现自动判断，中英互译
        return translate_weiruan(trans)
    else:
        return translate_weiruan(trans, fr='en', to='zh-CHS')


if __name__ == '__main__':
    # print('          翻译结果由微软翻译提供！（请确保网络已连接）')
    while True:
        start_translate("nihao")
        print('\n')
