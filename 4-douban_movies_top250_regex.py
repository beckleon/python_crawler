import requests
import re
import json


def write_to_json(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def parse_one_page(html):
    pattern = re.compile(
        '<em class="">(.*?)</em>.*?<div class="hd">.*?<a href="(.*?)".*?<span class="title">(.*?)</span>.*?<span class="title">(.*?)</span>.*?<span class="other">(.*?)</span>.*?<p class="">(.*?)<br>(.*?)</p>.*?property="v:average">(.*?)</span>.*?<span>(\d+)人评价</span>.*?<span class="inq">(.*?)</span>',
        re.S)
    items = pattern.findall(html)
    movie_list = []
    for item in items:
        movie = {}
        movie['index'] = item[0]
        movie['url'] = item[1].strip()
        movie['title_cn'] = item[2].strip()
        movie['title_ori'] = item[3].strip()
        movie['title_other'] = item[4].strip()

        # 处理 导演、演员
        staffs_list = item[5].strip().split("&nbsp;&nbsp;&nbsp;")
        director = staffs_list[0]
        if len(staffs_list) == 2:
            starrings = staffs_list[1]
        else:
            starrings = ""
        movie['director'] = director
        movie['starrings'] = starrings

        # 处理电影标签信息
        tags_list = item[6].strip().split("/")
        year = tags_list[0].replace("&nbsp;", "").strip()
        location = tags_list[1].replace("&nbsp;", "").strip()
        mtype = tags_list[2].replace("&nbsp;", "").strip()

        movie['year'] = year
        movie['location'] = location
        movie['mtype'] = mtype
        movie['score'] = item[7].strip()
        movie['reviews'] = item[8].strip()
        movie['quote'] = item[9].strip()

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


# 这里打印一下电影排名
#         print(item['index'], end='\t')
#     print("\n========================")


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 25)