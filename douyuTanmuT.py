import socket
import sys
import time
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
            contextDict[prSplit[0]]='0'
    return contextDict

def contentGet(context,tagStr):
    if context.find(tagStr):
        contextDict=content2Dict(context)
        return contextDict.get(tagStr,b'NONE').decode('utf-8','.ignore')
    else:
        return b'NONE'

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = '221.234.42.160'
    portid=8602
    sock.connect((address, portid))
    #
    rid=b'25515'
    gid=b'195'
    msg=b'type@=loginreq/username@kk=/password@kk=/roomid@='+rid+b'/\x00'
    sentmsg(sock,msg)
    print(sock.recv(1024))
    msg=b'type@=joingroup/rid@='+rid+b'/gid@='+gid+b'/\x00'
    sentmsg(sock,msg)

    while True:
        context=sock.recv(1024)
        tagStr = b'content'
        print(tagStr,'=',contentGet(context,tagStr))
    sock.close()

if __name__=='__main__':
    url= sys.argv[1] if len(sys.argv)>1 else 'http://www.douyutv.com/meizhi' 
    main()