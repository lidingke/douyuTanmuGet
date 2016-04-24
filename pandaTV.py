#!/usr/bin/env python3
# coding=utf-8
import urllib.request
import socket
import json
import time
import threading
import os
import platform
import sys
import re
import logging
import requests

import copy
import sqlite3
import traceback
import queue
import pickle


class PandaTV(threading.Thread):
    """docstring for PandaTV"""
    def __init__(self, roomid):
        super(PandaTV, self).__init__()
        threading.Thread.__init__(self)
        self.roomid = str(roomid)
        self.name = 'panda&' + self.roomid

        self.roomiddict={'10091':'囚徒','10029':'王师傅','31131':'SOL君','10027':'瓦莉拉','10025':'冰蓝飞狐','10003':'星妈'}

        self.CHATINFOURL = 'http://www.panda.tv/ajax_chatinfo?roomid='

        self.IGNORE_LEN = 16
        self.FIRST_REQ = b'\x00\x06\x00\x02'
        self.FIRST_RPS = b'\x00\x06\x00\x06'
        self.KEEPALIVE = b'\x00\x06\x00\x00'
        self.RECVMSG = b'\x00\x06\x00\x03'
        #BAMBOO_TYPE = '206'
        #AUDIENCE_TYPE = '207'
        self.SYSINFO = platform.system()
        #INIT_PROPERTIES = 'init.properties'
        #MANAGER = '60'
        #SP_MANAGER = '120'
        #HOSTER = '90'
        self.islive=True
        logging.basicConfig(filename = 'pandadanmulog.txt', filemode = 'a',
            level = logging.ERROR, format = '%(asctime)s - %(levelname)s: %(message)s')

        self.showQueue = queue.Queue()
        self.url = self.CHATINFOURL + self.roomid
        self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11\
         (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


    # def loadInit():
    #     with open(INIT_PROPERTIES, 'r') as f:
    #         init = f.read()
    #         init = init.split('\n')
    #         roomid = init[0].split(':')[1]
    #         #username = init[1].split(':')[1]
    #         #password = init[2].split(':')[1]
    #         return roomid


    def roomidDictGet(self):
        try:
            with open('roomiddict.pickle', 'rb') as f:
                self.roomiddict = pickle.load(f)
        except FileNotFoundError:
            self.roomiddict = {}
        except EOFError:
            self.roomiddict = {}

        self.roomidDictRe =  dict([(v,k) for k,v in self.roomiddict.items()])



    # def txtThread(self,*traceback):
    #     fadd=open("log.txt",'w')
    #     fadd.writelines(''.join(traceback))
    #     fadd.close()


    def notify(self,title, message):
        #about compatibility?
        if self.SYSINFO == 'Windows':
            pass
        elif self.SYSINFO == 'Linux':
            os.system('notify-send {}'.format(': '.join([title, message])))
        else:   #for mac
            t = '-title {!r}'.format(title)
            m = '-message {!r}'.format(message)
            os.system('terminal-notifier {} -sound default'.format(' '.join([m, t])))
    #             print(nickName + ":" + content)
    #             notify(nickName, content)


    def initSql(self):
        localTime=time.localtime()
        tyear=str(localTime.tm_year)
        tmoon=str(localTime.tm_mon) if len(str(localTime.tm_mon))==2 else '0'+str(localTime.tm_mon)
        tday=str(localTime.tm_mday) if len(str(localTime.tm_mday))==2 else '0'+str(localTime.tm_mday)
        dateNow=tyear+tmoon+tday
        sqlTableName='TM'+dateNow+'RD'+self.roomid
        conn = sqlite3.connect('pandadanmu.db')
        cursor = conn.cursor()
        try:
            strEx='create table if not exists '+sqlTableName+\
            ' (time int(10), name varchar(10), word varchar(50))'
            cursor.execute(strEx)
        except sqlite3.OperationalError as e:
            print('===sqlite3.OperationalError===')
            logging.exception(e)
        except :
            logging.exception( 'exception')
            # addException2logtxt(traceback)
        cursor.close()
        conn.commit()
        conn.close()
        return sqlTableName


    def save2Sql(self,sqlTableName,contentSql,snickSql,LocalTimeSql):
        conn = sqlite3.connect('pandadanmu.db')
        cursor = conn.cursor()
        try:
            while LocalTimeSql:
                strEx='insert into '+sqlTableName+' (time, name, word) values ('\
                    +str(LocalTimeSql[0])+',\''+snickSql[0]+'\',\''+contentSql[0]+'\')'
                cursor.execute(strEx)
                del(LocalTimeSql[0],snickSql[0],contentSql[0])
                #print(strEx)
            #print('===save to sql===')
        except sqlite3.OperationalError as e:
                print('panda danmu database is busy! data is not save')
                logging.exception(e)
        except Exception as e:
            # info=sys.exc_info()
            # # # print(info[0],":",info[1])
            # # print(info[1])
            logging.exception(e)
        cursor.close()
        conn.commit()
        conn.close()



    def KEEPALIVE(self,sock):
        while self.islive:
            print('====',self.roomiddict[self.roomid],' KEEPALIVE ===')
            sock.send(self.KEEPALIVE)
            for x in range(1,300):
                time.sleep(1)
                if self.islive is False:
                    return
                if self.isAlive is False:
                    return

    def log2server(self,ftag):
        try:
            data = ftag.text
            # print(data)
            # data = ftag.read().decode('utf-8')
            chatInfo = json.loads(data)
            chatAddr = chatInfo['data']['chat_addr_list'][0]
            socketIP = chatAddr.split(':')[0]
            socketPort = int(chatAddr.split(':')[1])
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = s
            s.connect((socketIP,socketPort))
            rid      = str(chatInfo['data']['rid']).encode('utf-8')
            appid    = str(chatInfo['data']['appid']).encode('utf-8')
            authtype = str(chatInfo['data']['authtype']).encode('utf-8')
            sign     = str(chatInfo['data']['sign']).encode('utf-8')
            ts       = str(chatInfo['data']['ts']).encode('utf-8')
            msg  = b'u:' + rid + b'@' + appid + b'\nk:1\nt:300\nts:' + ts + b'\nsign:' + sign + b'\nauthtype:' + authtype
            msgLen = len(msg)
            sendMsg = self.FIRST_REQ + int.to_bytes(msgLen, 2, 'big') + msg
            s.sendall(sendMsg)
            return s
        except ConnectionRefusedError:
            print('ConnectionRefusedError')
            logging.exception('ConnectionRefusedError')
            self.exit()

    def getChatInfo(self):
        roomid=self.roomid
        req = requests.get(self.url, headers=self.hdr)
        if req:
            req.encoding = 'utf-8'
            self.roomiddict[roomid]=self.roomiddict[roomid] if self.roomiddict.get(roomid) else  roomid
        # print('这里是主播：',self.roomiddict[roomid],'的直播间')
            # with urllib.request.urlopen(req) as f:
                #urllib.error.HTTPError
            s =  self.log2server(req)
            # s =  self.log2server(f)
            recvmsg = s.recv(4)
            if recvmsg == self.FIRST_RPS:
                print('成功连接弹幕服务器：',self.roomiddict[roomid])
                recvLen = int.from_bytes(s.recv(2), 'big')

            threading.Thread(target=PandaTV.KEEPALIVE,args=(self,s,)).start()

            sqlTableName=self.initSql()

            contentMsg=list()
            snickMsg=list()
            LocalMsgTime=list()

            while self.islive:
                try:
                    recvmsg = s.recv(4)
                except ConnectionAbortedError :
                    # logging.exception('ConnectionAbortedError')
                    self.exit()
                    #self.getChatInfo()
                if recvmsg == self.RECVMSG:
                    if s:
                        recvLen = int.from_bytes(s.recv(2), 'big')
                        recvmsg = s.recv(recvLen)   #ack:0
                        #print(self.RECVMSG)
                        recvLen = int.from_bytes(s.recv(4), 'big')
                        s.recv(self.IGNORE_LEN)
                        recvLen -= self.IGNORE_LEN
                        recvmsg = s.recv(recvLen)#chat msg
                        #print(self.RECVMSG)
                        recvmsg =recvmsg.split(b'{\"type\":')
                        for chatmsg in recvmsg[1:]:
                            typeContent = re.search(b'\"(\d+)\"',chatmsg)
                            #print(typeContent)
                            if typeContent:
                                if typeContent.group(1) == b'1':
                                    try:
                                        contentMsg.append(b''.join(re.findall(b'\"content\":\"(.*?)\"',chatmsg)).decode('unicode_escape'))
                                        snickMsg.append(b''.join(re.findall(b'\"nickName\":\"(.*?)\"',chatmsg)).decode('unicode_escape'))
                                        LocalMsgTime.append(int(time.time()))
                                        strprint =snickMsg[-1]+':'+contentMsg[-1]
                                        self.showQueue.put(strprint)
                                        # print(strprint)
                                    except :
                                        logging.exception('msg error')
                                        # threading.Thread(target=PandaTV.txtThread, args=(self,traceback,)).start()
                                elif typeContent.group(1) == b'207':
                                    contentSql=copy.deepcopy(contentMsg)
                                    snickSql=copy.deepcopy(snickMsg)
                                    LocalTimeSql=copy.deepcopy(LocalMsgTime)
                                    contentMsg.clear()
                                    snickMsg.clear()
                                    LocalMsgTime.clear()
                                    if len(contentSql) is not None:
                                        threading.Thread(target=PandaTV.save2Sql, args=(self,sqlTableName,contentSql,snickSql,LocalTimeSql,)).start()
                                elif typeContent.group(1) == b'206':
                                    goldNum=b''.join(re.findall(b'\"content\":\"(.*?)\"',chatmsg)).decode('unicode_escape')
                                    goldNikname=b''.join(re.findall(b'\"nickName\":\"(.*?)\"',chatmsg)).decode('unicode_escape')
                                    strprint=goldNikname+'送给主播'+goldNum+'个竹子'
                                    self.showQueue.put(strprint)
                                    #print(strprint)

            #print('close: ',s)
            if s:
                s.close()

    def show2cmd(self):
        while self.islive :
            while self.showQueue.empty() is not None :
                strprint = self.showQueue.get()
                try:
                    print(strprint)
                except UnicodeEncodeError:
                    logging.exception('===UnicodeEncodeError===')



    def run(self):
        #threading.Thread(target=PandaTV.show2cmd, args=(self,)).start()
        try:
            self.roomidDictGet()
            self.getChatInfo()
        except urllib.error.HTTPError:
            print('HTTPError')
            logging.exception('urllib.error.HTTPError')
            self.exit()
        except RuntimeError:
            print('RuntimeError')
            logging.exception('RuntimeError')
            self.exit()
        except ConnectionAbortedError:
            print('ConnectionAbortedError')
            logging.exception(ConnectionAbortedError)
            self.exit()
        except OSError:
            print('OSError')
            logging.exception('OSError')
            self.exit()



#
# get and set
#

    def exit(self):
        print('Thread:',self.roomiddict[self.roomid],'end')
        # if self.sock :
        #     pass
        try:
            self.sock.close()
        except AttributeError:
            pass
        self.islive = False

    def getRoomid(self):
        return self.roomid


    def setIslive(self,islive):
        print('Thread name = ',self.roomiddict[self.roomid],' inportIslive=',islive)
        self.islive=islive

    def getIslive(self):
        return self.islive


if __name__ == '__main__':
    idolid= sys.argv[1] if len(sys.argv)>1 else '66666'
    panda=PandaTV(idolid)
    panda.start()

    #python3 pandaTVDanmu.py 10091




