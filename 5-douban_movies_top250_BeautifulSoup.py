import requests
import re
import json
from bs4 import BeautifulSoup


def write_to_json(content):
    with open('result_beautifulsoup.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    list_soup = soup.find("div", class_="article").find_all("li")
    movie_list = []
    for item in list_soup:
        movie = {}
        # 排名
        index = item.find("em").get_text()
        # 属性值为info的div块
        info = item.find("div", class_="info")
        ## hd块
        hd = info.find("div", class_="hd")
        # 链接
        url = hd.a["href"]
        # 片名
        title_cn = title_ori = title_other = ''
        title_list = hd.a.find_all("span", class_="title")
        if len(title_list) == 2:
            title_cn = title_list[0].get_text().strip()
            title_ori = title_list[1].get_text().replace("\xa0", "").strip()
        else:
            title_cn = title_list[0].get_text().strip()

        title_o = hd.a.find("span", class_="other")
        if title_o:
            title_other = title_o.get_text().replace("\xa0", "").strip()

        ## bd块
        bd = info.find("div", class_="bd")
        # 文字块
        text_block = [text for text in bd.find("p", class_="").stripped_strings]
        # 处理 导演、演员
        staffs_list = text_block[0].split("\xa0\xa0\xa0")
        director = staffs_list[0].strip()
        if len(staffs_list) == 2:
            starrings = staffs_list[1].strip()
        else:
            starrings = ""
        # 处理电影标签信息
        tags_list = text_block[1].strip().split("/")
        year = tags_list[0].strip()
        location = tags_list[1].strip()
        mtype = tags_list[2].strip()

        # 评分
        score = bd.find("span", class_="rating_num").get_text()
        # 评价数 # 这里用正则表达式或者replace()函数
        span_list = bd.div.find_all("span")
        reviews = re.search('\d+', span_list[-1].get_text()).group()

        # 一句话影评
        quote = ""
        quote_block = bd.find("span", class_="inq")
        if quote_block:
            quote = quote_block.get_text()

        movie['index'] = index
        movie['url'] = url
        movie['title_cn'] = title_cn
        movie['title_ori'] = title_ori
        movie['title_other'] = title_other
        movie['director'] = director
        movie['starrings'] = starrings
        movie['year'] = year
        movie['location'] = location
        movie['mtype'] = mtype
        movie['score'] = score
        movie['reviews'] = reviews
        movie['quote'] = quote

        # 把movie字典加到列表中
        movie_list.append(movie)

    print(len(movie_list))
    return movie_list


def get_one_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def main(offset):
    url = 'https://movie.douban.com/top250?start={}&filter='.format(offset)
    html = get_one_page(url)

    for item in parse_one_page(html):
        write_to_json(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 25)