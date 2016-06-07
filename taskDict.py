
from collections import MutableMapping
from pandaTV import PandaTV
import threading


class MetaDict(MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)



class TaskDict(MetaDict):
    """use d[k] = v to put a thread into task dict
    v is the number of vistor,k is the roomid
    this dict put limit thread in and restart dead thread
    """
    def __init__(self, method = PandaTV, limit = 2000):
        super(TaskDict, self).__init__()
        self.method = method
        self.limit = limit
        print('create TaskDict',method,'limit=',limit)
        # self.arg = arg

    def __setitem__(self, key, number):
        # print('get k,v',key,number,'type',type(key),type(number))
        if not isinstance(number,int):
            number = int(number)
        if number > self.limit:
            # print('put in ',key,number)
            self.__putIn(key)
        else:
            if key in self.store.keys():
                self.store[key].exit()
                del self.store[key]


    def __putIn(self,key):
        if key not in self.store.keys():
            value = self.method(key)
            self.store[key] = value
            value.start()
        else:
            value = self.store[key]
            if value.isAlive() is False:
                value = self.method(key)
                self.store[key] = value
                value.start()

if __name__ == '__main__':
    t = TaskDict()
    t[1] = '12'
    print(t)

