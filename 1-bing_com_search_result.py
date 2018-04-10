#encoding=utf8

#This is a test demo for getting search results(title and url) from Bing.com
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
	'pq':'李大爷',
	'q':'李大爷',
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
        print(h2.select('a')[0].get_text())
        print(h2.a.attrs['href'])
        print("=============")
        
