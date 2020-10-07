import json
import requests

from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent" : "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language" : "en-us",
    "Connection" : "keep-alive",
    "Accept-Charset" : "GB2312,utf-8;q=0.7,*;q=0.7"
}

s = requests.Session()
s.headers = HEADERS


def get_page(url):
    html = s.get(url).text
    return html


def get_all_pages():
    url_base = "https://match.lottery.sina.com.cn/lotto/pc_zst/index?lottoType=dlt&actionType=chzs&year={year}"
    year = 2020
    year_longest = 2007
    htmls = list()

    while year >= year_longest:
        url = url_base.format(year=year)
        print(f"Getting: {url}")
        htmls.append(get_page(url))
        year -= 1

    return htmls


def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    data = list()

    for tr in soup.find_all("tr"):
        charball_select = "td[class*=chartball]"
        if not tr.select(charball_select):
            continue

        cur = list()
        cur.append(tr.select("td")[0].text)
        for td in tr.select(charball_select):
            cur.append(td.text)
        data.append(cur)

    return data

if __name__ == '__main__':
    data = list()
    for page in get_all_pages():
        data += parse_page(page)

    print(len(data))

    with open("dlt_data.json", "w") as fp:
        fp.write(json.dumps(data))
