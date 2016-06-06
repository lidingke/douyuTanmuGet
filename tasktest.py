import threading
import time
import random


class Task(threading.Thread):
    """docstring for Task"""
    def __init__(self, roomid):
        super(Task, self).__init__()
        # self.arg = arg
        self.roomid = roomid
        self.alive = True
        self.number = 0

    def run(self):
        while self.alive:
            self.number = random.uniform(20, 100)
            time.sleep(10)

            if random.uniform(1,10) >8:
                raise RuntimeError
            if random.uniform(1,10) >8:
                self.alive = False



if __name__ == '__main__':
    tasklist = []
    for x in range(1,10):
        tasklist.append(['1000'+str(x),random.uniform(20,100)])


