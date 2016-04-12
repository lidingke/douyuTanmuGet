import requests
import traceback
import pickle
import logging
from lxml import etree
import sys
import sqlite3
import time
from pandaTV import PandaTV
from pandaspider import PandaSpider
import copy
import threading
import pdb

class DouyuSpider(PandaSpider):
    """docstring for DouyuSpider"""
    def __init__(self):
        super(DouyuSpider, self).__init__()
        # self.arg = arg
        self.url = 'http://www.douyu.com/directory/game/How'

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
            print(self.number)
            roomidElement = selector.xpath('//*[@id="live-list-contentbox"]/li')#atribute

            self.roomid = [x.attrib.get('data-rid') for x in roomidElement]
            # pdb.set_trace()
            print('douyu')
            print('获取',len(self.name),'条name信息',len(self.title),'条title信息',len(self.number),'条number信息',len(self.roomid),'条roomid信息。')

if __name__ == '__main__':
    try:
        panda = DouyuSpider()
        panda.requestData()
    except Exception as e:
        logging.exception(e)
