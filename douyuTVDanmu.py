import socket
import sys
import time
import uuid
import hashlib

import requests
import re
import sys

def staticGet(idolid):
    hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    url='http://www.douyutv.com/'+idolid
    print(url)
    html = requests.get(url,headers = hea).text
    roomid = "".join(re.findall('task_roomid" value="(\d+)',html))
    titleStr = "".join(re.findall('"server_config":"%5B%7B(.*?)%7D%5D","def_disp_gg":0};',html))
    titleStr = re.sub('%22','',titleStr)
    listTitle = titleStr.split('%7D%2C%7B')
    logServer=dict()
    logServer['port']=''.join(re.findall('%2Cport%3A(\d+)',listTitle[2]))
    logServer['ip']=''.join(re.findall('ip%3A(.*?)%2C',listTitle[2]))
    logServer['rid']=roomid
    return logServer




# def content2Dict(context):
#     context = context.split(b'/')
#     contextDict=dict()
#     for pr in context:
#         prSplit=pr.split(b'@=')
#         if len(prSplit)>1:         
#             contextDict[prSplit[0]]=prSplit[1]
#         else:
#             contextDict[prSplit[0]]=b'-1'
#     return contextDict

# def contentGet(context,tagStr):
#     if context.find(tagStr):
#         contextDict=content2Dict(context)
#         return contextDict.get(tagStr,b'-1').decode('utf-8','.ignore')
#     else:
#         return '-1'

def danmuServerGet(sockStr):
    contextList=sockStr.split(b'\x00"')[0].split(b'\xb2\x02')
    for cl in contextList:
        danmuServer=dict()
        cl=cl.decode('utf-8','.ignore')
        if cl.find('msgrepeaterlist'):
            clstr=''.join(re.findall('list@=(.*?)/',cl))
            for ls in clstr.split('@S'):
                danmuIp=''.join(re.findall('Sip@AA=(.*?)@',ls))
                danmuPort=''.join(re.findall('Sport@AA=(\d+)',ls))
                danmuServer[danmuPort]=danmuIp
                #print(danmuIp,danmuPort)
        if cl.find('setmsggroup'):
            danmuServer['gid']=re.findall('gid@=(\d+)/',cl)
            danmuServer['rid']=re.findall('rid@=(.*?)/',cl)
    return danmuServer

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

def dynamicGet(logServer):
    address = logServer.get('ip')
    portid = logServer.get('port')
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
    rid=logServer.get('rid')
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
        #print(context)
        danmuServer=danmuServerGet(context)
        print(danmuServer['gid'])
    else:
        danmuServer=dict()
    sock.close()
    #returnDict={'isError':typeID1st,'typeID':typeID2st,'gid':gid,,}

    return danmuServer

def danmuWhile(danmuServer):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = b'danmu.douyutv.com'
    portid=8602
    sock.connect((address, portid))
    rid=''.join(danmuServer.get('rid'))
    rid=rid.encode('utf-8')
    gid=''.join(danmuServer.get('gid'))
    gid=gid.encode('utf-8')
    msg=b'type@=loginreq/username@=/password@=/roomid@='+rid+b'/\x00'
    sentmsg(sock,msg)
    sock2st=sock.recv(1024)
    msg=b'type@=joingroup/rid@='+rid+b'/gid@='+gid+b'/\x00'
    sentmsg(sock,msg)
    while True:
        chatmsg=sock.recv(1024)
        if chatmsg.find(b'chatmessage'):
            contentMsg=b''.join(re.findall(b'content@=(.*?)/',chatmsg))
            snickMsg=b''.join(re.findall(b'@Snick@A=(.*?)@',chatmsg))
            print(snickMsg.decode('utf-8'),':',contentMsg.decode('utf-8'))
        else:
            print('-1')
    sock.close()

def main(idolid):

    logServer=staticGet(idolid)
    danmuServer=dynamicGet(logServer)
    print(danmuServer.get('gid'),danmuServer.get('rid'))
    danmuWhile(danmuServer)


if __name__=='__main__':
    idolid= sys.argv[1] if len(sys.argv)>1 else 'http://www.douyutv.com/imbabbc' 
    main(idolid)