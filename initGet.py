import socket
import sys
import time
import uuid
import hashlib

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

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = '119.90.49.101'
    portid=8003
    sock.connect((address, portid))
    #
    devid=uuid.uuid1().hex.swapcase().encode('utf-8')
    intTime=int(time.time())
    rt=str(intTime).encode('utf-8')
    hashvk = hashlib.md5()
    vk=rt+b'7oE9nPEG9xXV69phU31FYCLUagKeYtsF'+devid
    hashvk.update(vk)
    vk = hashvk.hexdigest().encode('utf-8')
    username = b'visitor2432'
    password = b'123456'
    rid=b'16789'
    gid=b''#b'195'
    msg=b'type@=loginreq'\
    +b'/username@='+username\
    +b'/ct@=0'\
    +b'/password@='+password\
    +b'/roomid@='+rid\
    +b'/devid@='+devid\
    +b'/rt@='+rt\
    +b'/vk@='+vk\
    +b'/ver@=20150929'\
    +b'/\x00'
    print(msg)
    sentmsg(sock,msg)
    print(sock.recv(1024))
    context=sock.recv(1024)
    print(context)
    gid=contentGet(context,b'gid').encode('utf-8')
    print(gid)
    #msg=b'type@=joingroup/rid@='+rid+b'/gid@='+gid+b'/\x00'
    #sentmsg(sock,msg)
    #context=sock.recv(1024)
    #print(context)


    #context=sock.recv(1024)
    #print(context)
    #context=sock.recv(1024)
    #print(context)
 #   while context.find(b'error'):
#        context=sock.recv(1024)
#        tagStr = b'rid'
#        contentGet(context,tagStr)

    sock.close()

if __name__=='__main__':
    url= sys.argv[1] if len(sys.argv)>1 else 'http://www.douyutv.com/meizhi' 
    main()