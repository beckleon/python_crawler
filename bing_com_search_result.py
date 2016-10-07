#encoding=utf8

#This is a test demo for getting search results(title and url) from Bing.com
#search keyword:王师傅
##############################
#pre-installed packages:
#----pip install requests
#----pip install BeautifulSoup4
#----pip install lxml
##############################

import requests
from bs4 import BeautifulSoup

payload={
	'cvid':'8E816F936C6C42718FD27E4F64B659B9',
	'form':'QBLH',
	'pq':'王师傅',
	'q':'王师傅',
	'qs':'n',
	'sc':'8-3',
	'sk':'',
	'sp':'-1'
}

headers={
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'en-US,en;q=0.5',
	'Connection':'keep-alive',
	'Host':'cn.bing.com',
	'Referer':'http://cn.bing.com/',
	'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0'
}

url="http://cn.bing.com/search?"
r=requests.get(url, params=payload, headers=headers)

#use BeautifulSoup to analyse the response page
soup= BeautifulSoup(r.text, 'lxml')
#print soup.prettify()

lis = soup.find_all("li",attrs={"class":"b_algo"})

for li in lis:
    for h2 in li.select("h2"):
	print h2.select('a')[0].get_text()
	print h2.a.attrs['href']
        print "============="
        
############result like:###############
'''
王师傅不玩牧师了的微博_微博
http://www.weibo.com/u/5341832954
=============
“王师傅是卖鞋的”正确答案 - 百度经验—— …
http://jingyan.baidu.com/article/414eccf611bdc06b421f0a4a.html
=============
王师傅直播间_熊猫直播_最娱乐的直播平台
http://www.panda.tv/10029
=============
王师傅是卖鞋的,一双鞋进价30元甩卖20元,顾 …
http://zuoye.baidu.com/question/cc085ed0f56876856be9915cb64eb71d.html
=============
王师傅吧_百度贴吧
http://tieba.baidu.com/f?kw=%E7%8E%8B%E5%B8%88%E5%82%85&ie=utf-8
=============
村口王师傅是什么东西_dnf魔道吧_百度贴吧
http://tieba.baidu.com/p/2622191072
=============
王师傅酒楼电话,地址,价格,营业时间(图)-武汉- …
http://www.dianping.com/shop/548837
=============
郑州千层饼的做法郑州王师傅千层饼的制作方 …
http://jingyan.baidu.com/article/6b97984d8b9edd1ca2b0bfcf.html
=============
'''
