import requests
import re
import json
from lxml import etree


def write_to_json(content):
    with open('result_xpath.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def parse_one_page(html):
    doc = etree.HTML(html)
    item_list = doc.xpath('//div[@class="article"]//li')
    movie_list = []
    for item in item_list:
        movie = {}
        # 排名
        index = item.xpath('./div/div[1]/em/text()')[0]
        # 属性值为info的div块
        info = item.xpath('./div/div[@class="info"]')[0]
        ## hd块
        hd = info.xpath('./div[@class="hd"]')[0]
        # 链接
        url = hd.xpath('./a/@href')[0]
        # 片名
        title_cn = title_ori = title_other = ''
        title_list = hd.xpath('./a/span[@class="title"]')
        if len(title_list) == 2:
            title_cn = title_list[0].xpath('./text()')[0].strip()
            title_ori = title_list[1].xpath('./text()')[0].replace("\xa0", "").strip()
        else:
            title_cn = title_list[0].xpath('./text()')[0].strip()

        title_o = hd.xpath('./a/span[@class="other"]')
        if title_o:
            title_other = title_o[0].xpath('./text()')[0].replace("\xa0", "").strip()

        ## bd块
        bd = info.xpath('./div[@class="bd"]')[0]
        # 文字块
        text_block = bd.xpath('./p[@class=""]/text()')
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
        score = bd.xpath('./div/span[@class="rating_num"]/text()')[0]
        # 评价数 # 这里用正则表达式或者replace()函数
        reviews = re.search('\d+', bd.xpath('./div/span[last()]/text()')[0]).group()

        # 一句话影评
        quote = ""
        quote_block = bd.xpath('.//span[@class="inq"]')
        if quote_block:
            quote = quote_block[0].xpath('./text()')[0]

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


# 这里打印一下电影排名
#         print(item['index'], end='\t')
#     print("\n========================")


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 25)