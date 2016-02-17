import requests
from lxml import etree

hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
url='http://www.douyutv.com/qiuri'
print('connect url:',url)
html = requests.get(url,headers = hea)
selector = etree.HTML(html.text)
content = selector.xpath('//*[@id="weighttit"]')

for x in content:
	print(x.text)