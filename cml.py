from mulpro import God
from pandaspider import PandaSpider
from pandaTV import PandaTV

from douyuspider import DouyuSpider
from douyuTV import DouyuTV

import sys


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv)>1 else 'None'
    rid = sys.argv[1] if len(sys.argv)>1 else None
    if cmd == 'douyuGuard':
        God(DouyuSpider()).run()
    elif cmd =='pandaGuard':
        God(PandaSpider()).run()
    elif cmd == 'douyuDanmu':
        roomid= rid if len(rid)>1 else '48699'
        DouyuTV(roomid,show=True).start()
    elif cmd == 'pandaDanmu':
        roomid= rid if len(rid)>1 else '66666'
        PandaTV(roomid,show=True).start()
    elif cmd == 'douyuNoGuard':
        DouyuSpider.run()
    elif cmd == 'pandaNoGuard':
        PandaSpider.run()
    else:
        print('Command is not found')
