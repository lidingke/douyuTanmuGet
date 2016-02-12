import requests
import re
import sys

def testFun():
    return 'error'

def main():
    url = 'http://www.douyutv.com/16789'
    hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    html = requests.get(url,headers = hea).text
    titleStr = "".join(re.findall('"server_config":"%5B%7B(.*?)%7D%5D","def_disp_gg":0};',html))
    titleStr = re.sub('%22','',titleStr)
    listTitle = titleStr.split('%7D%2C%7B')
    ipPortDict=dict()
    for lp in listTitle:
        ipPortDict["".join(re.findall('%2Cport%3A(\d+)',lp))]="".join(re.findall('ip%3A(.*?)%2C',lp))
        print(lp)
    for k,v in ipPortDict.items():
        print(k,v)
    errorID='ture'
    while errorID!='error':

        errorID=testFun()
        print(errorID)


if __name__=='__main__':
#url= sys.argv[1] if len(sys.argv)>1 else 'http://www.douyutv.com/meizhi' 
    main()