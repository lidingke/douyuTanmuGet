import socket
import sys
import time
import uuid
import hashlib

import requests
import re
import sys

def staticGet(url):
    hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    html = requests.get(url,headers = hea).text
    titleStr = "".join(re.findall('"server_config":"%5B%7B(.*?)%7D%5D","def_disp_gg":0};',html))
    titleStr = re.sub('%22','',titleStr)
    listTitle = titleStr.split('%7D%2C%7B')
    ipPortDict=dict()
    for lp in listTitle:
        ipPortDict["".join(re.findall('%2Cport%3A(\d+)',lp))]="".join(re.findall('ip%3A(.*?)%2C',lp))
#    for k,v in ipPortDict.items():
#        print(k,v)
    return ipPortDict


def sentmsg(sock,msg) :
    data_length= len(msg)+8
    code=689
    msgHead=int.to_bytes(data_length,4,'little')\
        +int.to_bytes(data_length,4,'little')+int.to_bytes(code,4,'little')
    sock.send(msgHead)
    sent=0
    while sent<len(msg):
        tn= sock.send(msg[sent:])
        sent= sent + tn

def content2Dict(context):
    context = context.split(b'/')
    contextDict=dict()
    for pr in context:
        prSplit=pr.split(b'@=')
        if len(prSplit)>1:         
            contextDict[prSplit[0]]=prSplit[1]
        else:
            contextDict[prSplit[0]]=b'-1'
    return contextDict

def contentGet(context,tagStr):
    if context.find(tagStr):
        contextDict=content2Dict(context)
        return contextDict.get(tagStr,b'-1').decode('utf-8','.ignore')
    else:
        return '-1'

def dynamicGet(address,portid):
    

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((address, int(portid)))
    print(address,portid)
    #
    devid=uuid.uuid1().hex.swapcase()
    rt=str(int(time.time()))
    hashvk = hashlib.md5()
    vk=rt+'7oE9nPEG9xXV69phU31FYCLUagKeYtsF'+devid
    #print(vk)
    hashvk.update(vk.encode('utf-8'))
    vk = hashvk.hexdigest()
    username = ''
    password = ''
    rid='16789'
    gid=''#b'195'
    msg='type@=loginreq'\
    +'/username@='+username\
    +'/ct@=0'\
    +'/password@='+password\
    +'/roomid@='+rid\
    +'/devid@='+devid\
    +'/rt@='+rt\
    +'/vk@='+vk\
    +'/ver@=20150929'\
    +'/\x00'
    #print(msg)
    sentmsg(sock,msg.encode('utf-8'))
    context=sock.recv(1024)
    #print(context)
    context=context.split(b'\xb2\x02')[1].decode('utf-8')
    typeID1st=re.findall('type@=(.*?)/',context)[0]
    if typeID1st != 'error' :
        sentmsg(sock,msg.encode('utf-8'))
        context=sock.recv(1024)
        print(context)
        context=context.split(b'\xb2\x02')[1]#.decode('utf-8')
        if re.findall(b'msgrepeaterlist',context):
            returnDict =content2Dict(context)
        #returnlist[0]=typeID2st

    else:
        returnDict=dict()
    sock.close()
    #returnDict={'isError':typeID1st,'typeID':typeID2st,'gid':gid,,}

    return returnDict

def main():

    url = 'http://www.douyutv.com/16789'
    ipPortDict=staticGet(url)
    for k,v in ipPortDict.items():
        print(k,v)
        getDict=dynamicGet(v,k)
        for dk,dv in getDict.items():
            print(dk,dv)
        break




if __name__=='__main__':
    url= sys.argv[1] if len(sys.argv)>1 else 'http://www.douyutv.com/meizhi' 
    main()