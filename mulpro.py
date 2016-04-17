from multiprocessing import Process
# import threading
# from testtr import test
from douyuspider import DouyuSpider
from pandaspider import PandaSpider
import time
import pdb

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
                self.process = Process(target=self.guestpro)
                self.process.start()


if __name__ == '__main__':
    God(PandaSpider()).run()
    time.sleep(100)
    God(DouyuSpider()).run()
    # g.run()




