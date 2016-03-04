import requests
import re
hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64)\
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
idolid='board'
url='http://www.douyutv.com/'+idolid
print('connect url:',url)
html = requests.get(url,headers = hea).text
showStatus=re.search("\"show_status\":(\d+),\"",html)
if showStatus:
	print(showStatus.group(1))
	pass

