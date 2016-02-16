import socket
import sys
import time
import uuid
import hashlib

import requests
import re
import sys
import threading



def staticGet(idolid):
    hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    url='http://www.douyutv.com/'+idolid
    print('connect url:',url)
    html = requests.get(url,headers = hea).text
    roomid = "".join(re.findall('task_roomid" value="(\d+)',html))
    titleStr = "".join(re.findall('"server_config":"%5B%7B(.*?)%7D%5D","def_disp_gg":0};',html))
    titleStr = re.sub('%22','',titleStr)
    listTitle = titleStr.split('%7D%2C%7B')
    logServer=dict()
    logServer['port']=''.join(re.findall('%2Cport%3A(\d+)',listTitle[2]))
    logServer['ip']=''.join(re.findall('ip%3A(.*?)%2C',listTitle[2]))
    logServer['rid']=roomid
    print('Logserver,port:',logServer['port'],'ip:',logServer['ip'],'rid:',logServer['rid'])
    return logServer


def danmuServerGet(sockStr):
    contextList=sockStr.split(b'\x00"')[0].split(b'\xb2\x02')
    danmuServer=dict()
    for cl in contextList:
        cl=cl.decode('utf-8','.ignore')
        if re.search('msgrepeaterlist',cl):
            danmuServer['add']=re.findall('Sip@AA=(.*?)@',cl)
            danmuServer['port']=re.findall('Sport@AA=(\d+)',cl)
        elif re.search('setmsggroup',cl):
            danmuServer['gid']=re.findall('gid@=(\d+)/',cl)
            danmuServer['rid']=re.findall('rid@=(.*?)/',cl)
    print('danmuServer adress:',danmuServer['add'][0],danmuServer['port'][0],'groupID:',danmuServer['gid'])
    return danmuServer

def sendmsg(sock,msgstr) :
    msg=msgstr.encode('utf-8')
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
    devid=uuid.uuid1().hex.swapcase()
    rt=str(int(time.time()))
    hashvk = hashlib.md5()
    vk=rt+'7oE9nPEG9xXV69phU31FYCLUagKeYtsF'+devid
    hashvk.update(vk.encode('utf-8'))
    vk = hashvk.hexdigest()
    username = ''
    password = ''
    rid=logServer.get('rid')
    gid=''
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
    sendmsg(sock,msg)
    context=sock.recv(1024)
    #print(context)
    context=context.split(b'\xb2\x02')[1].decode('utf-8')
    typeID1st=re.findall('type@=(.*?)/',context)[0]
    if typeID1st != 'error' :
        sendmsg(sock,msg)
        context=sock.recv(1024)
        #print(context)
        danmuServer=danmuServerGet(context)
        print('group ID get:',danmuServer['gid'])
    else:
        danmuServer=dict()
    sock.close()
    #returnDict={'isError':typeID1st,'typeID':typeID2st,'gid':gid,,}

    return danmuServer

def danmuWhile(danmuServer):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = danmuServer['add'][0]
    portid=int(danmuServer.get('port')[0])
    sock.connect((address, portid))
    rid=''.join(danmuServer.get('rid'))
    #rid=rid.encode('utf-8')
    gid=''.join(danmuServer.get('gid'))
    #gid=gid.encode('utf-8')
    msg='type@=loginreq/username@=/password@=/roomid@='+rid+'/\x00'
    sendmsg(sock,msg)
    sock2st=sock.recv(1024)
    msg='type@=joingroup/rid@='+rid+'/gid@='+gid+'/\x00'
    whileCodition=True
    def keepalive():
        print('===init keepalive===')
        while whileCodition:
            print('40sleep')
            msg='type@=keeplive/tick@='+str(int(time.time()))+'/\x00'
            sendmsg(sock,msg)
            time.sleep(40)
        sock.close()

    threading.Thread(target=keepalive).start()
    sendmsg(sock,msg)
    print('danmu proccessing')
    
    while whileCodition:
        chatmsg=sock.recv(1024)
        print(chatmsg)
        typeContent = re.search(b'type@=(.*?)/',chatmsg)
        if typeContent:
            if typeContent.group(1) == b'chatmessage':
                #print(chatmsg.find(b'chatmessage'))
                contentMsg=b''.join(re.findall(b'content@=(.*?)/',chatmsg))
                snickMsg=b''.join(re.findall(b'@Snick@A=(.*?)@',chatmsg))
                LocalMsgTime=str(int(time.time()))
                print(contentMsg)
                if snickMsg==b'\xe4\xb8\x81\xe6\x9e\x9c' and contentMsg[:4]==b'exit':
                    print('==========get break target======')
                    whileCodition=False
                #print(contentMsg,":",snickMsg)
                try:
                    msgprint=snickMsg+b':'+contentMsg
                    msgprint=msgprint.decode('utf-8',"replace")
                    print(msgprint)
                except :
                    print('===GBK encode error, perhaps special string ===')
            elif typeContent.group(1) == b'keeplive':
                #timeReturn=b''.join(re.findall(b'tick@=(\d+)/',keeplive))
                pass
            else:
                pass

    sock.close()

def main(idolid):

    logServer=staticGet(idolid)
    danmuServer=dynamicGet(logServer)
    #print(danmuServer.get('gid'),danmuServer.get('rid'))
    danmuWhile(danmuServer)


if __name__=='__main__':
    idolid= sys.argv[1] if len(sys.argv)>1 else '16789'
    main(idolid)
#python3 douyuTVDanmu.py lushicheng    