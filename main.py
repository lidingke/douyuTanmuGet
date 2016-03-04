import sys
from douyuTV import DouyuTV



if __name__=='__main__':
    idolid= sys.argv[1] if len(sys.argv)>1 else 'yilidi'
    douyu=DouyuTV(idolid)
    douyu.show()
#python3 douyuTVDanmu.py 16789
