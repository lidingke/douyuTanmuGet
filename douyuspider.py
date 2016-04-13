import requests
import pickle
import logging
from lxml import etree
import sys
import pdb
import sqlite3
import time
from douyuTV import DouyuTV
import threading

class DouyuSpider(object):
    """docstring for douyuSpider"""
    def __init__(self):
        super(DouyuSpider, self).__init__()
        self.url = 'http://www.douyu.com/directory/game/How'
        self.numTop = 10000
        self.reloadtime = 30
        self.name = list()
        self.title = list()
        self.number = list()
        self.roomid = list()
        self.hotStarData = list()
        self.dbName = 'douyuData.db'
        self.roomidsave = 'douyuRoomid.pickle'
        self.threadList = list()
        self.newThreadList = list()
        self.roomiddict={}
        # self.threadList[0] = ['roomid','number','threadID']
        logging.basicConfig(filename = 'douyuspiderlog.txt', filemode = 'a',
            level = logging.ERROR, format = '%(asctime)s - %(levelname)s: %(message)s')
        self.roomidPickleInit()
        self.threadDict = {}
        self.isLive = True
        self.aliveThread = list()

    # def logException(self):


    def roomidPickleInit(self):
        self.roomiddict = dict()
        try:
            with open(self.roomidsave, 'rb') as f:
                self.roomiddict = pickle.load(f)
        except FileNotFoundError:
            with open(self.roomidsave, 'wb') as f1:
                entryinit = {}
                pickle.dump(entryinit, f1)
            with open(self.roomidsave, 'rb') as f2:
                self.roomiddict = pickle.load(f2)

    def roomidPickleSave(self):
        print('save a roomid.pickle len = ',len(self.roomiddict))
        with open(self.roomidsave, 'wb') as f:
            pickle.dump(self.roomiddict, f)


    def requestData(self):
        try:
            r = requests.get(self.url)
        except Exception as e:
            raise e
            # # print(traceback)
            # logging.exception(e)
            # time.sleep(30)
            # self.requestData()
        else:
            r.encoding = 'utf-8'
            selector = etree.HTML(r.text)
            self.name = selector.xpath('//*[@id="live-list-contentbox"]/li/a/div/p/span[1]/text()')
            self.title = selector.xpath('//*[@id="live-list-contentbox"]/li/a/div/div/h3/text()')
            strnumber = selector.xpath('//*[@id="live-list-contentbox"]/li/a/div/p/span[2]/text()')
            self.number = list()
            for num in strnumber:
                if num.find('万') > 0:
                    # pdb.set_trace()
                    self.number.append(int(eval(num[:-1])*10000))
                else:
                    self.number.append(int(num))
            # print(self.number)
            roomidElement = selector.xpath('//*[@id="live-list-contentbox"]/li')#atribute
            self.roomid = [x.attrib.get('data-rid') for x in roomidElement]
            # pdb.set_trace()
            # print('douyu')
            print('获取',len(self.name),'条name信息',len(self.title),'条title信息',len(self.number),'条number信息',len(self.roomid),'条roomid信息。')


    def hotStarDataGet(self):
        if self.hotStarData:
            self.hotStarData.clear()
        while self.name :
            name = self.name.pop()
            title = self.title.pop()
            number = self.number.pop()
            roomid = self.roomid.pop()
            if int(number) > self.numTop:
                self.hotStarData.append({'name':name,'title':title,'number':number,'roomid':roomid})
            self.roomiddict[roomid] = name
        # print(self.hotStarData)

    def save2sql(self):
        for star in self.hotStarData:
            # pdb.set_trace()
            conn = sqlite3.connect(self.dbName)
            cursor = conn.cursor()
            nowTime = str(int(time.time()))
            sqlTableName = 'dTV' + star['roomid']
            try:
                strEx='create table if not exists '+sqlTableName+' (time int(10) primary key, name varchar(10),\
                title varchar(20), number varchar(10), roomid varchar(10))'
                cursor.execute(strEx)
                strEx = "insert into " + sqlTableName + "(time, name, title, number, roomid) values ("\
                + nowTime+ ",' " + star['name'] + " ' , ' " + star['title'] + " ' , ' " + str(star['number']) + " ' , ' " + star['roomid'] +" ' )"

                #print(strEx)
                cursor.execute(strEx)
            except sqlite3.OperationalError as e:
                print(self.dbName,e)
            except sqlite3.IntegrityError as e :
                strEx = "insert into " + sqlTableName + "( number ) values (" + star['number'] + ")"
                print(strEx)
                cursor.execute(strEx)
            #except sqlite3.OperationalError as e:
            cursor.close()
            conn.commit()
            conn.close()


    def initTreadDict(self):
        # pdb.set_trace()
        for star in self.hotStarData:
            threadAdd = DouyuTV(star['roomid'])
            threadAdd.setDaemon(True)
            # print('检测',star['roomid'],type(star),type(star['roomid']))
            time.sleep(1)
            threadAdd.start()
            self.threadDict[threadAdd.getName()] = threadAdd
            # pdb.set_trace()
            print(self.roomiddict[threadAdd.getName()[6:]],'线程初始化')
            #douyu thread name = "douyu&" + roomid
        print(len(self.hotStarData),'个弹幕记录线程初始化')


    def newThreadCreate(self):
        newThreadDict = dict()
        killTread = list()
        reThreadDict = dict()
        for star in self.hotStarData:
            newThreadDict[star['roomid']] = star['number']
        # old thread checker
        for threadName,threadAdd in self.threadDict.items():
            roomid = threadName[6:]
            #restart Dead thread
            if newThreadDict.pop(roomid,False) is not False:

                if threadAdd.isAlive() is False:
                    print('need to recreat:',self.roomiddict[roomid],'线程状态为',threadAdd.isAlive())
                    # time.sleep(1)
                    reThreadAdd = DouyuTV(roomid)
                    reThreadAdd.setDaemon(True)
                    reThreadAdd.start()
                    print('recreat:',self.roomiddict[roomid],'线程状态变为',
                        reThreadAdd.isAlive())
                    reThreadDict[roomid] = reThreadAdd
            else:
                #kill down hot room
                threadAdd.exit()
                killTread.append(threadName)
                print('kill:',self.roomiddict[roomid],'线程状态变为',
                    threadAdd.isAlive())

        print('newthreaddict：',len(newThreadDict))

        # del dead thread in self.threadict
        for deltread in killTread:
            self.threadDict.pop(deltread)
        # reload thread in self.threaddict
        for k,v in reThreadDict.items():
            if self.threadDict.get(k):
                self.threadDict[k] = v
        # new thread creater
        if newThreadDict:
            for newName,hotNumber in newThreadDict.items():
                threadAdd = DouyuTV(newName)
                threadAdd.setDaemon(True)
                if self.threadDict.get('douyu&'+str(newName),False) is False:
                    # time.sleep(1)
                    threadAdd.start()
                    self.threadDict[threadAdd.getName()] = threadAdd
                    print('creat:',self.roomiddict[newName],'新线程启动状态为',
                        threadAdd.isAlive())

    def getAliveThread(self):
        self.allAliveThread = threading.enumerate()
        if self.aliveThread:
            self.aliveThread.clear()
        # print(self.allAliveThread)
        for x in self.allAliveThread:
            name = x.getName()[:5]
            if name == 'douyu':
                self.aliveThread.append(x)
        #print(self.aliveThread)
        print('thread num :',len(self.aliveThread))




    def show(self):
        print('人气超过',str(self.numTop),'的有',len(self.hotStarData),'人')

            # if x is '':
            #     pass
        #print(self.hotStarData['name'])
        #for star in self.hotStarData:
            # print(star['name'],'的人气为：',star['number'])

    def exit(self):
        self.isLive = False
        print('exit DouyuTV')


    def spiderProccess(self):
        """
        main proccess
        """

        self.requestData()
        self.hotStarDataGet()
        self.save2sql()
        self.show()

        self.initTreadDict()
        # pdb.set_trace()
        self.roomidPickleSave()

        while self.isLive:
            #
            self.requestData()
            self.hotStarDataGet()
            self.save2sql()
            self.show()
            self.getAliveThread()
            if self.hotStarData:
                # if the hot star is none,
                # keep the last thread alive none newthread create
                self.newThreadCreate()
            time.sleep(self.reloadtime)




if __name__ == '__main__':
    try:
        douyu = DouyuSpider()
        douyu.spiderProccess()
    except Exception as e:
        logging.exception(e)


#python douyuspider.py

