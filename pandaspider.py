import requests
import traceback
import pickle
import logging
from lxml import etree
import sys
import sqlite3
import time
from pandaTV import PandaTV
import copy
import threading

class PandaSpider(object):
    """docstring for pandaSpider
    game = 'hearthstone'
    this is the default game, the last address of game area
    """
    def __init__(self,game = 'hearthstone'):
        super(PandaSpider, self).__init__()
        self.url = 'http://www.panda.tv/cate/'+game
        # self.url = 'http://www.panda.tv/cate/lol'
        self.numTop = 2000
        self.reloadtime = 30
        self.name = list()
        self.title = list()
        self.number = list()
        self.roomid = list()
        self.hotStarData = list()
        self.dbName = 'pandaData.db'
        self.threadList = list()
        self.newThreadList = list()
        self.roomiddict={'10091':'囚徒','10029':'王师傅','31131':'SOL君','10027':'瓦莉拉','10025':'冰蓝飞狐','10003':'星妈'}
        # self.threadList[0] = ['roomid','number','threadID']
        logging.basicConfig(filename = 'spiderlog.txt', filemode = 'a',
            level = logging.ERROR, format = '%(asctime)s - %(levelname)s: %(message)s')
        self.roomidPickleInit()
        self.threadDict = {}
        self.isLive = True
        self.aliveThread = list()

    # def logException(self):


    def roomidPickleInit(self):
        self.roomiddict = dict()
        try:
            with open('roomiddict.pickle', 'rb') as f:
                self.roomiddict = pickle.load(f)
        except FileNotFoundError:
            with open('roomiddict.pickle', 'wb') as f1:
                entryinit = {'10091':'囚徒','10029':'王师傅','31131':'SOL君',
                '10027':'瓦莉拉','10025':'冰蓝飞狐','10003':'星妈'}
                pickle.dump(entryinit, f1)
            with open('roomiddict.pickle', 'rb') as f2:
                self.roomiddict = pickle.load(f2)

    def roomidPickleSave(self):
        print('save a roomid.pickle len = ',len(self.roomiddict))
        with open('roomiddict.pickle', 'wb') as f:
            pickle.dump(self.roomiddict, f)


    def requestData(self):
        try:
            r = requests.get(self.url)
        except Exception as e:
            # print(traceback)
            logging.exception(e)
            time.sleep(30)
            self.requestData()
        else:
            r.encoding = 'utf-8'
            selector = etree.HTML(r.text)
            self.name = selector.xpath('//*[@id="sortdetail-container"]/li/a/div[3]/span[1]/text()')
            self.title = selector.xpath('//*[@id="sortdetail-container"]/li/a/div[2]/text()')
            self.number = selector.xpath('//*[@id="sortdetail-container"]/li/a/div[3]/span[2]/text()')
            roomidElement = selector.xpath('//*[@id="sortdetail-container"]/li/a')#atribute
            self.roomid = [x.get('data-id') for x in roomidElement]
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

    def save2sql(self):
        for star in self.hotStarData:
            conn = sqlite3.connect(self.dbName)
            cursor = conn.cursor()
            nowTime = str(int(time.time()))
            sqlTableName = 'pTV' + star['roomid']
            try:
                strEx='create table if not exists '+sqlTableName+' (time int(10) primary key, name varchar(10),\
                title varchar(20), number varchar(10), roomid varchar(10))'
                cursor.execute(strEx)
                strEx = "insert into " + sqlTableName + "(time, name, title, number, roomid) values ("\
                + nowTime+ ",' " + star['name'] + " ' , ' " + star['title'] + " ' , ' " + star['number'] + " ' , ' " + star['roomid'] +" ' )"

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
        for star in self.hotStarData:
            threadAdd = PandaTV(star['roomid'])
            threadAdd.setDaemon(True)
            #print('检测',star['roomid'],type(star),type(star['roomid']))
            time.sleep(1)
            threadAdd.start()
            self.threadDict[threadAdd.getName()] = threadAdd
            print(self.roomiddict[threadAdd.getName()[6:]],'线程初始化')
            #panda thread name = "panda&" + roomid
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
                    reThreadAdd = PandaTV(roomid)
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
                threadAdd = PandaTV(newName)
                threadAdd.setDaemon(True)
                if self.threadDict.get('panda&'+str(newName),False) is False:
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
            if name == 'panda':
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
        print('exit pandaTV')


    def spiderProccess(self):
        """
        main proccess
        """

        self.requestData()
        self.hotStarDataGet()
        self.save2sql()
        self.show()
        self.initTreadDict()
        self.roomidPickleSave()

        while self.isLive:

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

    def run(self):
        try:
            # douyu = DouyuSpider()
            self.spiderProccess()
        except IOError as e:
            logging.exception(e)
        except RuntimeError as e:
            logging.exception(e)
            self.exit()
        except Exception as e:
            logging.exception(e)



if __name__ == '__main__':
    try:
        panda = PandaSpider()
        panda.spiderProccess()
    except Exception as e:
        logging.exception(e)
        panda.exit()


#python pandaspider.py

