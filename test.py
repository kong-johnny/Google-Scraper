import requests
from bs4 import BeautifulSoup
link = 'https://ipofferings.com/patents-for-sale-drones-uavs.php'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}
res = requests.get(link, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, 'html.parser')
print(soup.get_text())
# content = soup.select_one('body').get_text()
# print(content)
