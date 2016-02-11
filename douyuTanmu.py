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

def contentGet(context):
    print('ifcontent=',context.find(b'content'))
    #print(context)
    context = context.split(b'/')
    contextDict=dict()
    for pr in context:
        prSplit=pr.split(b'@=')
        if len(prSplit)>1:         
            contextDict[prSplit[0]]=prSplit[1]
            #print(prSplit[0],b':',prSplit[1])
        else:
            contextDict[prSplit[0]]='0'
    return contextDict.get(b'content','NONE').decode('utf-8')
    

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = '221.234.42.159'
    portid=8602
    sock.connect((address, portid))
    roomid=b'208114'
    msg=b'type@=loginreq/username@kk=/password@kk=/roomid@='+roomid+b'/\x00'
    sentmsg(sock,msg)
    print(sock.recv(1024))
    msg=b'type@=joingroup/rid@='+roomid+b'/gid@=186/'+b'\x00'
    sentmsg(sock,msg)
    while True:
        context=sock.recv(1024)
        print('content=',contentGet(context))
    sock.close()

if __name__=='__main__':
    url= sys.argv[1] if len(sys.argv)>1 else 'http://www.douyutv.com/meizhi' 
    main()