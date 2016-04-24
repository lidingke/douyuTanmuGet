from crawguard import CrawlerGuard
import requests
from lxml import etree
import logging
from multiprocessing import Process
import time


class DouyuGuard(CrawlerGuard):
    """docstring for DouyuGuard"""
    def __init__(self, platform = 'douyu', area = 'How'):
        super(DouyuGuard, self).__init__(platform,area)
        self.platform = platform
        self.area = area
        self.numTop = 10000

    def requestData(self):
        try:
            r = requests.get(self.url)
            print(self.url)
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

class PandaGuard(CrawlerGuard):
    """docstring for PandaGuard"""
    def __init__(self, platform = 'panda', area = 'hearthstone'):
        super(PandaGuard, self).__init__(platform,area)
        self.platform = platform
        self.area = area
        self.numTop = 2000

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



class God(object):
    """docstring for God"""
    def __init__(self, guest):
        super(God, self).__init__()
        self.guest = guest
        self.process = Process(target=self.guestpro)
        self.process.start()
        print('process start')

    def guestpro(self):
        self.guest.run()

    def run(self):
        while True:
            time.sleep(60)
            if self.process.is_alive() == False:
                print('restart')
                self.process.terminate()
                self.process = Process(target=self.guestpro)
                self.process.start()


if __name__ == '__main__':
    # from mulpro import God
    p = PandaGuard()
    p.run()
    # God(PandaGuard()).run()
