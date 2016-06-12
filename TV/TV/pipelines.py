# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html




# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi              #导入twisted的包
import MySQLdb
import MySQLdb.cursors
from scrapy.conf import settings
from TV.items import TvItem
import pdb

class TvPipeline(object):
    def __init__(self):                            #初始化连接mysql的数据库相关信息
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                db = settings['MYSQL_DBNAME'],
                user = settings['MYSQL_USER'],
                passwd = settings['MYSQL_PASSWD'],
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = False
        )

    # pipeline dafault function                    #这个函数是pipeline默认调用的函数
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        return item

    # insert the data to databases                 #把数据插入到数据库中
    def _conditional_insert(self, tx, item):
        # pdb.set_trace()
        sql = "create table if not exists {} (\
        name varchar(10),title varchar(10),\
        roomid varchar(10),number varchar(10))".format(settings['MYSQL_TABLE'])
        # item = TvItem()
        # print(sql)
        tx.execute(sql)
        for x in item['source']:
            # pdb.set_trace()
            sql = "insert into {} values (\'{}\', \'{}\', \'{}\', \'{}\')".format(
                settings['MYSQL_TABLE'],
                x[0].encode('utf-8'),
                x[1].encode('utf-8'),
                x[2].encode('utf-8'),
                x[3].encode('utf-8'))
            # print(sql)
            tx.execute(sql)
