import requests
from bs4 import BeautifulSoup
import csv
from trans import trans
import time
from tqdm import tqdm


def google_search(keyword, num_results, page_st=1):
    # 设置请求头信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }

    # 初始化结果列表
    results = []
    page = page_st-1

    # 循环请求每一页的结果
    while len(results) < num_results:
        # 计算每页的起始位置
        start = page * 10
        print(f"正在爬取第 {page + 1} 页的结果，起始位置为 {len(results)}...")

        # 构造分页请求的URL
        search_url = f"https://www.google.com/search?q={keyword}&start={start}"

        # 发送GET请求
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取搜索结果
        search_results = soup.select('.g')

        # 遍历搜索结果并保存标题和链接
        for result in tqdm(search_results):
            if result.select_one('.LC20lb.DKV0Md') is None:
                continue
            # 提取标题
            title = result.select_one('.LC20lb.DKV0Md').get_text()

            # 提取链接
            link = result.select_one('.yuRUbf a')['href']

            # 提取描述
            description = result.select_one('.VwiC3b.MUxGbd').get_text()

            # 页面内容
            try:
                res = requests.get(link, headers=headers)
                res.raise_for_status()
                soup = BeautifulSoup(res.text, 'html.parser')
                content = soup.get_text()
                content = content.split('\n')
                # 内容中多个空格、换行符替换为一个空格
                content = [' '.join(it.split()) for it in content if it != '' and it != ' ']
                # 合并内容为字符串数组，每个字符串不超过5000字符
                tmp = []
                st = ""
                for it in content:
                    if len(st + " " + it) > 5000:
                        tmp.append(st)
                        st = ""
                    st += " " + it
                if st != "":
                    tmp.append(st)
                content = tmp


            except Exception as e:
                content = "无法获取页面内容"

            # 添加标题和链接到结果列表
            results.append({'标题': title, '链接': link, '描述': description, '内容': content})

            if len(results) == num_results:
                break
        page += 1

    return results


def save_to_csv(results):
    filename = input("请输入保存的文件名（不包含扩展名.csv）：") + ".csv"

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['标题', '标题翻译', '链接', '描述', '描述翻译', '内容', '内容翻译'])
        writer.writeheader()
        writer.writerows(results)

    print(f"结果已保存到文件 {filename}")


def translate(results):
    # 调用函数实现标题翻译
    for result in results:
        result['标题翻译'] = trans(result['标题'])
        result['描述翻译'] = trans(result['描述'])
        result['内容翻译'] = []
        for content in result['内容']:
            result['内容翻译'].append(trans(content))
        result['内容翻译'] = '\n'.join(result['内容翻译'])
    return results


while True:
    # 调用函数进行搜索并限制结果数量
    keyword = input("请输入关键词: ")
    num_results = int(input("请输入要爬取的记录条数: "))
    page_start_from = int(input("请输入开始爬取的页数: "))
    st = time.time()
    search_results = google_search(keyword, num_results, page_start_from)

    search_results = translate(search_results)

    for i in range(len(search_results)):
        search_results[i]['内容'] = '\n'.join(search_results[i]['内容'])

    ed = time.time()
    print(f"爬取完成，耗时 {ed - st} 秒")
    # 输出结果
    for result in search_results:
        print(f"原标题：{result['标题']}")
        print(f"翻译后标题：{result['标题翻译']}")
        print(f"链接：{result['链接']}")
        print(f"描述：{result['描述']}")
        print(f"翻译后描述：{result['描述翻译']}")
        if len(result['内容']) > 100:
            print(f"内容：{result['内容'][:100]}...（更多内容保存后查看！！）")
            print(f"翻译后内容：{result['内容翻译'][:100]}...（更多内容保存后查看！！）")
        else:
            print(f"内容：{result['内容']}")
            print(f"翻译后内容：{result['内容翻译']}")
        print()

    # 询问是否保存结果到CSV文件
    save_option = input("是否保存结果到CSV文件？(y/n): ")

    if save_option.lower() == 'y':
        save_to_csv(search_results)

    ck = input("退出？(y/n): ")
    if ck.lower() == 'y' or ck.lower() == 'yes':
        break
