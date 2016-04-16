from multiprocessing import Process
# import threading
# from testtr import test
from douyuspider import DouyuSpider
from pandaspider import PandaSpider
import time
import pdb

class god(object):
    """docstring for god"""
    def __init__(self, guest):
        super(god, self).__init__()
        self.guest = guest
        self.process = Process(target=self.guestpro)
        self.process.start()
        print('process start')



    def guestpro(self):
        # self.guest = DouyuSpider()
        self.guest.run()
        # t.run()
        # pass

    def warcher(self):
        while True:
            time.sleep(30)
            if self.process.is_alive() == False:
                print('restart')
                self.process = Process(target=self.guestpro)
                self.process.start()


    def run(self):
        # pass
        self.warcher()
        # threading.Thread(target = god.t,).start()




if __name__ == '__main__':
    god(PandaSpider()).run()
    time.sleep(100)
    god(DouyuSpider()).run()
    # g.run()




