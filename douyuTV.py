#!/usr/bin/env python3
# coding=utf-8

import socket
import sys
import time
import uuid
import hashlib

import requests
from lxml import etree
import re
import sys
import threading
import pickle
import copy
import sqlite3
import queue
import logging


class DouyuTV(threading.Thread):
    """docstring for DouyuTV"""
    def __init__(self, roomid):
        super(DouyuTV, self).__init__()
        threading.Thread.__init__(self)
        self.roomid = str(roomid)
        self.name = 'douyu&' + self.roomid
        self.islive = True
        self.logServer={'status':'0'}
        self.danmuServer={'add':'danmu.douyutv.com','port':'12602','gid':'1','rid':str(roomid)}
        self.sock=None
        self.sqlfileName = 'douyudanmu.db'
        self.danmuStatus =True
        self.sqlTableName = 'TM0000RD0000'
        self.showQueue = queue.Queue()
        self.html = None
        logging.basicConfig(filename = 'log.txt', filemode = 'a',
            level = logging.ERROR, format = '%(asctime)s - %(levelname)s: %(message)s')

        self.hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive'}

    def islive(self,islive):
        self.islive = islive


    def roomidDictGet(self):
        try:
            with open('douyuRoomid.pickle', 'rb') as f:
                self.roomiddict = pickle.load(f)
        except FileNotFoundError:
            self.roomiddict = {}
        except EOFError:
            self.roomiddict = {}

        self.roomidDictRe =  dict([(v,k) for k,v in self.roomiddict.items()])


    # def staticGet(self):
    #     hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64)\
    #      AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    #     url='http://www.douyutv.com/'+self.roomid
    #     self.html = requests.get(url,headers = hea).text
    #     html =self.html
    #     print('connect url:',url)
    #     roomid = "".join(re.findall('task_roomid" value="(\d+)',html))
    #     titleStr = "".join(re.findall('"server_config":"%5B%7B(.*?)%7D%5D","def_disp_gg":0};',html))
    #     titleStr = re.sub('%22','',titleStr)
    #     listTitle = titleStr.split('%7D%2C%7B')
    #     self.logServer['status']='1'
    #     self.logServer['port']=''.join(re.findall('%2Cport%3A(\d+)',listTitle[2]))
    #     self.logServer['ip']=''.join(re.findall('ip%3A(.*?)%2C',listTitle[2]))
    #     self.logServer['rid']=roomid
    #     print('self.logServer,port:',self.logServer['port'],'ip:',self.logServer['ip'],'rid:',self.logServer['rid'])

    def staticRequests(self):
        # hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64)\
        #  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
        hea = self.hdr
        url='http://www.douyutv.com/'+self.roomid
        try:
            req = requests.get(url,headers = hea)
            if req:
                req.encoding = 'utf-8'
                # req = requests.get(url,headers = hea)
                #req.encoding = 'utf-8'
                self.selector = etree.HTML(req.text)
                task_roomid = self.selector.xpath('//*[@id="task_roomid"]')[0]
                show_status = self.selector.xpath('/html/head/script[2]/text()')[0]
                room_container = self.selector.xpath('//*[@id="room_container"]/script[4]/text()')[0]
                # room_container = port and host
                task_roomid = task_roomid.get('value')
                room_container = str(room_container)
                show_status=re.search("\"show_status\":(\d+),\"",show_status).group(1)
                titleStr = "".join(re.findall('"server_config":"%5B%7B(.*?)%7D%5D","def_disp_gg":0};',room_container))
                titleStr = re.sub('%22','',titleStr)
                listTitle = titleStr.split('%7D%2C%7B')
                self.logServer['status']=show_status
                self.logServer['port']=''.join(re.findall('%2Cport%3A(\d+)',listTitle[2]))
                self.logServer['ip']=''.join(re.findall('ip%3A(.*?)%2C',listTitle[2]))
                self.logServer['rid']=task_roomid
                # print('logServer,port:',self.logServer['port'],'ip:',self.logServer['ip'],'rid:',self.logServer['rid'],'show_status:',show_status)
        except Exception:
            self.logServer = {'status':'1','port':'8022','ip':'119.90.49.105','rid':self.roomid}

        # if showStatus:
        #     if showStatus.group(1)=='1':
        #         print('connect url:',url)
        #         roomid = "".join(re.findall('task_roomid" value="(\d+)',html))
        #         titleStr = "".join(re.findall('"server_config":"%5B%7B(.*?)%7D%5D","def_disp_gg":0};',html))
        #         titleStr = re.sub('%22','',titleStr)
        #         listTitle = titleStr.split('%7D%2C%7B')
        #         self.logServer['status']='1'
        #         self.logServer['port']=''.join(re.findall('%2Cport%3A(\d+)',listTitle[2]))
        #         self.logServer['ip']=''.join(re.findall('ip%3A(.*?)%2C',listTitle[2]))
        #         self.logServer['rid']=roomid
        #         print('self.logServer,port:',self.logServer['port'],'ip:',self.logServer['ip'],'rid:',self.logServer['rid'])
        #     else:
        #         print('该主播没有直播')
        #         self.logServer['status']='2'
        # else:
        #         print('找不到页面')
        #         self.logServer['status']='2'

    def statusGet(self):
        return self.logServer['status']


    def stop(self):
        self.islive = False


    # def danmuStatus(self,danmState):
    #     while self.danmuStatus and danmState:
    #         print('===show status get===')
    #         hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64)\
    #          AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    #         url='http://www.douyutv.com/'+roomid
    #         html = requests.get(url,headers = hea).text
    #         showStatus=re.search("\"show_status\":(\d+),\"",html)
    #         if showStatus:
    #             if showStatus.group(1)=='1':
    #                 time.sleep(60)
    #             else:
    #                 self.islive=False



    def danmuServerGet(self,sockStr):
        contextList=sockStr.split(b'\x00"')[0].split(b'\xb2\x02')

        for cl in contextList:
            cl=cl.decode('utf-8','.ignore')
            if re.search('msgrepeaterlist',cl):
                self.danmuServer['add']=re.findall('Sip@AA=(.*?)@',cl)
                self.danmuServer['port']=re.findall('Sport@AA=(\d+)',cl)
            elif re.search('setmsggroup',cl):
                self.danmuServer['gid']=re.findall('gid@=(\d+)/',cl)
                self.danmuServer['rid']=re.findall('rid@=(.*?)/',cl)
        print('self.danmuServer adress:',self.danmuServer['add'][0],\
            self.danmuServer['port'][0],'groupID:',self.danmuServer['gid'])


    def sendmsg(self,msgstr) :
        msg=msgstr.encode('utf-8')
        data_length= len(msg)+8
        code=689
        msgHead=int.to_bytes(data_length,4,'little')\
            +int.to_bytes(data_length,4,'little')+int.to_bytes(code,4,'little')
        self.sock.send(msgHead)
        sent=0
        while sent<len(msg):
            tn= self.sock.send(msg[sent:])
            sent= sent + tn


    def dynamicGet(self):
        address = self.logServer.get('ip')
        portid = self.logServer.get('port')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address, int(portid)))
        devid=uuid.uuid1().hex.swapcase()
        rt=str(int(time.time()))
        hashvk = hashlib.md5()
        vk=rt+'7oE9nPEG9xXV69phU31FYCLUagKeYtsF'+devid
        hashvk.update(vk.encode('utf-8'))
        vk = hashvk.hexdigest()
        username = ''
        password = ''
        rid=self.logServer.get('rid')
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
        # print(msg)
        self.sendmsg(msg)
        context=self.sock.recv(1024)
        # print(context)
        context=context.split(b'\xb2\x02')[1].decode('utf-8')
        typeID1st=re.findall('type@=(.*?)/',context)[0]
        if typeID1st != 'error' :
            self.sendmsg(msg)
            context=self.sock.recv(1024)
            # print(context)
            self.danmuServerGet(context)
            # print('group ID get:',self.danmuServer['gid'])
        else:
            self.danmuServer['gid']='-1'
        self.sock.close()
        #returnDict={'isError':typeID1st,'typeID':typeID2st,'gid':gid,,}


    def keeplive(self):
        print('===init keeplive===')
        while self.islive :
            #print('40sleep')
            msg='type@=keeplive/tick@='+str(int(time.time()))+'/\x00'
            try:
                self.sendmsg(msg)
            except OSError:
                self.exit()

            #keeplive=sock.recv(1024)
            time.sleep(20)
        self.sock.close()

    def save2Sql(self,contentSql,snickSql,LocalTimeSql):
        # print('===insql')
        conn = sqlite3.connect(self.sqlfileName)
        cursor = conn.cursor()
        while LocalTimeSql:
            strEx='insert into '+self.sqlTableName+' (time, name, word) values ('\
                +str(LocalTimeSql[0])+',\''+snickSql[0]+'\',\''+contentSql[0]+'\')'
            try:
                cursor.execute(strEx)
            # except Exception:
            except sqlite3.OperationalError:
                print('danmu database is busy! data is not save')
            except Exception as e:
                logging.exception(e)

            del(LocalTimeSql[0],snickSql[0],contentSql[0])
        cursor.close()
        conn.commit()
        conn.close()
        # print('===save===')


    def danmuWhile(self):
        contentMsg=list()
        snickMsg=list()
        LocalMsgTime=list()
        while self.islive:
            try:
                chatmsgLst=self.sock.recv(1024).split(b'\xb2\x02')
            except ConnectionAbortedError:
                return
            #print(chatmsgLst)
            for chatmsg in chatmsgLst[1:]:
                typeContent = re.search(b'type@=(.*?)/',chatmsg)
                if typeContent:
                    if typeContent.group(1) == b'chatmsg':
                        try:
                            contentMsg.append(b''.join(re.findall(b'txt@=(.*?)/',chatmsg)).decode('utf-8',"replace"))
                            snickMsg.append(b''.join(re.findall(b'nn@=(.*?)/',chatmsg)).decode('utf-8',"replace"))
                            LocalMsgTime.append(int(time.time()))
                            strprint = snickMsg[-1]+':'+contentMsg[-1]
                            self.showQueue.put(strprint)
                        except :
                            print('===GBK encode error, perhaps special string ===')
                    elif typeContent.group(1) == b'keeplive':
                        contentSql=copy.deepcopy(contentMsg)
                        snickSql=copy.deepcopy(snickMsg)
                        LocalTimeSql=copy.deepcopy(LocalMsgTime)
                        contentMsg=list()
                        snickMsg=list()
                        LocalMsgTime=list()
                        threading.Thread(target=DouyuTV.save2Sql, args=(self,contentSql,snickSql,LocalTimeSql,)).start()


    def danmuProcce(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = self.danmuServer['add'][0]
        portid=int(self.danmuServer.get('port')[0])
        self.sock.connect((address, portid))
        rid=''.join(self.danmuServer.get('rid'))
        gid=''.join(self.danmuServer.get('gid'))
        msg='type@=loginreq/username@=/password@=/roomid@='+rid+'/\x00'
        self.sendmsg(msg)
        sock2st=self.sock.recv(1024)

        msg='type@=joingroup/rid@='+rid+'/gid@='+gid+'/\x00'
        self.sendmsg(msg)

        threading.Thread(target=DouyuTV.keeplive, args=(self,)).start()
        # print('danmu proccessing')
        #open SQL
        localTime=time.localtime()
        tyear=str(localTime.tm_year)
        tmoon=str(localTime.tm_mon) if len(str(localTime.tm_mon))==2 else '0'+str(localTime.tm_mon)
        tday=str(localTime.tm_mday) if len(str(localTime.tm_mday))==2 else '0'+str(localTime.tm_mday)
        dateNow=tyear+tmoon+tday
        conn = sqlite3.connect(self.sqlfileName)
        cursor = conn.cursor()
        self.sqlTableName='TM'+dateNow+'RD'+rid
        strEx='create table if not exists '+self.sqlTableName+\
        ' (time int(10), name varchar(10), word varchar(50))'
        cursor.execute(strEx)
        cursor.close()
        conn.commit()
        conn.close()

        self.danmuWhile()

        self.sock.close()

    def show2cmd(self):
        while self.islive :
            while self.showQueue.empty() is not None :
                strprint = self.showQueue.get()
                try:
                    print(strprint)
                except UnicodeEncodeError:
                    logging.exception('===UnicodeEncodeError===')

    # def show(self):

    #     self.staticRequests()
    #     #threading.Thread(target=DouyuTV.DouyuTV.danmuStatus, args=(self,)).start()
    #     # print(self.logServer['status'])
    #     # # if self.logServer['status']=='2':
    #     # #     return -1
    #     self.dynamicGet()
    #     try:
    #         self.danmuProcce()
    #     except InterruptedError :
    #         self.islive=False
    def exit(self):
        print('Thread:',self.name,'end')
        try:
            self.sock.close()
        except AttributeError:
            pass
        self.islive = False


    def run(self):
        # threading.Thread(target=PandaTV.show2cmd, args=(self,)).start()
        self.roomidDictGet()
        self.staticRequests()
        self.dynamicGet()
        try:
            self.danmuProcce()
        except InterruptedError :
            self.islive=False



if __name__=='__main__':
    roomid= sys.argv[1] if len(sys.argv)>1 else '48699'
    douyu=DouyuTV(roomid)
    douyu.start()



