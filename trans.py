import requests


def trans(query):
    url = 'http://fanyi.youdao.com/translate'
    data = {
        "i": query,  # 待翻译的字符串
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": "16081210430989",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_CLICKBUTTION"
    }
    try:
        res = requests.post(url, data=data).json()
        tra = ""
        for i in res['translateResult'][0]:
            if i['tgt'] is not None:
                tra = tra + " " + i['tgt']
        return tra
    except Exception as e:
        return '翻译出错'

# main('你好') # 输出: hello
