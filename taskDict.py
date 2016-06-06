
from collections import MutableMapping


class TaskDict(MutableMapping):
    """docstring for TaskDict"""
    def __init__(self,):
        super(TaskDict, self).__init__()




if __name__ == '__main__':
    t = TaskDict()
    t['1'] = '12'
    print(t)

