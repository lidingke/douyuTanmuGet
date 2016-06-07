import pickle
import logging
import sys
import sqlite3
import time
from pandaTV import PandaTV
import threading
import abc
from taskDict import TaskDict
import pdb



class CrawlerGuard(object):
    """docstring for CrawlerGuard
    abstract factory pattern
    subclass need to rewrite requestData()
    """
    __metaclass__  = abc.ABCMeta
    def __init__(self, platform = 'panda', area = 'hearthstone'):
        super(CrawlerGuard, self).__init__()
        self.platform = platform
        self.area = area
        # self.crawname = platform + '_' +area
        # self.url = 'http://www.panda.tv/cate/hearthstone'
        self.url = self.urlCreater(platform, area)
        self.numTop = 2000
        self.reloadtime = 10
        self.name = list()
        self.title = list()
        self.number = list()
        self.roomid = list()
        self.hotStarData = list()
        self.dbName = platform+'Data.db'
        # self.threadList = list()
        # self.newThreadList = list()
        self.hotStarDict = {}
        self.taskDict = TaskDict(self.method,self.numTop)
        # self.method =
        self.roomiddict={}
        self.roomidpickle = platform+'roomid.pickle'
        # self.threadList[0] = ['roomid','number','threadID']
        logging.basicConfig(filename = 'log\{}_guardlog.txt'.format(self.platform), filemode = 'a',
            level = logging.ERROR, format = '%(asctime)s - %(levelname)s: %(message)s')
        self.roomidPickleInit()
        self.threadDict = {}
        self.isLive = True
        self.aliveThread = list()

    # def logException(self):

    def urlCreater(self, platform = 'panda', area = 'lol'):
        urldict = {'panda':'http://www.panda.tv/cate/','douyu':'http://www.douyu.com/directory/game/'}
        return urldict[platform]+area

    def roomidPickleInit(self):
        picklename = self.roomidpickle
        try:
            with open(picklename, 'rb') as f:
                self.roomiddict = pickle.load(f)
        except FileNotFoundError:
            with open(picklename, 'wb') as f1:
                entryinit = {}
                pickle.dump(entryinit, f1)
            with open(picklename, 'rb') as f2:
                self.roomiddict = pickle.load(f2)

    def roomidPickleSave(self):
        picklename = self.roomidpickle
        print('save a roomid.pickle len = ',len(self.roomiddict))
        with open(picklename, 'wb') as f:
            pickle.dump(self.roomiddict, f)

    @abc.abstractmethod
    def requestData(self):
        '''request html and return name title number and roomid as a list
        '''

    def save2sql(self):
        for star in self.hotStarData:
            conn = sqlite3.connect(self.dbName)
            cursor = conn.cursor()
            nowTime = str(int(time.time()))
            sqlTableName = self.platform +'TV' + star['roomid']
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
                strEx = "insert into " + sqlTableName + "( number ) values (" + str(star['number']) + ")"
                print(strEx)
                cursor.execute(strEx)
            #except sqlite3.OperationalError as e:
            cursor.close()
            conn.commit()
            conn.close()



    def hotStarDataGet(self):
        # print(self.hotStarData)
        if self.hotStarData:
            self.hotStarData.clear()
        for x,v in enumerate(self.name):
            # pdb.set_trace()
            self.hotStarData.append({'name':self.name[x],
                'title':self.title[x],
                'number':self.number[x],
                'roomid':self.roomid[x]})
            # pdb.set_trace()
            # print(self.hotStarData['name'])
            # self.roomiddict[roomid] = name
            # pdb.set_trace()

            # self.taskDict[self.roomid[x]] = int(self.number[x])

        self.newThreadCreate()

    def newThreadCreate(self):
        ''' Task dict is a mode to test limite and create new thread
        '''
        delkey = None
        if self.hotStarData:
            for x in self.hotStarData:
                self.hotStarDict[x['roomid']] = x['number']
            for k,v in self.hotStarDict.items():
                self.taskDict[k] = v
                if self.hotStarDict[k] == -1:
                    delkey = k
                else:
                    self.hotStarDict[k] = -1
            if delkey:
                self.hotStarDict.pop(delkey)



    # def initTreadDict(self):
    #     for star in self.hotStarData:
    #         threadAdd = PandaTV(star['roomid'])
    #         threadAdd.setDaemon(True)
    #         #print('检测',star['roomid'],type(star),type(star['roomid']))
    #         time.sleep(1)
    #         threadAdd.start()
    #         self.threadDict[threadAdd.getName()] = threadAdd
    #         print(self.roomiddict[threadAdd.getName()[6:]],'线程初始化')
    #         #panda thread name = "panda&" + roomid
    #     print(len(self.hotStarData),'个弹幕记录线程初始化')


    # def newThreadCreate(self):
    #     newThreadDict = dict()
    #     killTread = list()
    #     reThreadDict = dict()
    #     for star in self.hotStarData:
    #         newThreadDict[star['roomid']] = star['number']
    #     # old thread checker
    #     for threadName,threadAdd in self.threadDict.items():
    #         roomid = threadName[6:]
    #         #restart Dead thread
    #         if newThreadDict.pop(roomid,False) is not False:

    #             if threadAdd.isAlive() is False:
    #                 print('need to recreat:',self.roomiddict[roomid],'线程状态为',threadAdd.isAlive())
    #                 # time.sleep(1)
    #                 reThreadAdd = PandaTV(roomid)
    #                 reThreadAdd.setDaemon(True)
    #                 reThreadAdd.start()
    #                 print('recreat:',self.roomiddict[roomid],'线程状态变为',
    #                     reThreadAdd.isAlive())
    #                 reThreadDict[roomid] = reThreadAdd
    #         else:
    #             #kill down hot room
    #             threadAdd.exit()
    #             killTread.append(threadName)
    #             print('kill:',self.roomiddict[roomid],'线程状态变为',
    #                 threadAdd.isAlive())

    #     print('newthreaddict：',len(newThreadDict))

    #     # del dead thread in self.threadict
    #     for deltread in killTread:
    #         self.threadDict.pop(deltread)
    #     # reload thread in self.threaddict
    #     for k,v in reThreadDict.items():
    #         if self.threadDict.get(k):
    #             self.threadDict[k] = v
    #     # new thread creater
    #     if newThreadDict:
    #         for newName,hotNumber in newThreadDict.items():
    #             threadAdd = PandaTV(newName)
    #             threadAdd.setDaemon(True)
    #             if self.threadDict.get(self.platform+'&'+str(newName),False) is False:
    #                 # time.sleep(1)
    #                 threadAdd.start()
    #                 self.threadDict[threadAdd.getName()] = threadAdd
    #                 print('creat:',self.roomiddict[newName],'新线程启动状态为',
    #                     threadAdd.isAlive())


    def getAliveThread(self):
        allAliveThread = threading.enumerate()
        print('allAliveThread num',len(allAliveThread))
        if self.aliveThread:
            self.aliveThread.clear()
        # print(allAliveThread)
        for x in allAliveThread:
            name = x.getName()[:5]
            if name == self.platform:
                self.aliveThread.append(x)
        #print(self.aliveThread)
        print('spider num :',len(self.aliveThread),'dict num:',len(self.taskDict))
        # if len(self.aliveThread) > len(self.threadDict):
        #     raise AssertionError('spider num ERROR')


    def show(self):
        print('人气超过',str(self.numTop),'的有',len(self.taskDict),'人')

            # if x is '':
            #     pass
        #print(self.hotStarData['name'])
        #for star in self.hotStarData:
            # print(star['name'],'的人气为：',star['number'])

    def exit(self):
        self.isLive = False
        print('exit pandaTV')


    def start(self):
        """
        main proccess
        """
        while self.isLive:
            self.requestData()
            self.hotStarDataGet()
            self.save2sql()
            self.show()
            self.getAliveThread()
            # if self.hotStarData:
                # if the hot star is none,
                # keep the last thread alive none newthread create
            # self.newThreadCreate()
            time.sleep(self.reloadtime)

    def run(self):
        try:
            # douyu = DouyuSpider()
            self.start()
        except IOError as e:
            logging.exception(e)
            raise e
        except RuntimeError as e:
            logging.exception(e)
            self.exit()
            raise e
        except AssertionError as e:
            logging.exception(e)
            self.exit()
            raise e
        except Exception as e:
            logging.exception(e)
            raise e


# class DanmuThread(threading.Thread):
#     """docstring for DanmuThread"""
#     def __init__(self):
#         super(DanmuThread, self).__init__()
#         self.arg = arg

