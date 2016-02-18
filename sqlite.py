#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import time
# 连接到SQLite数据库
# 数据库文件是test.db
# 如果文件不存在，会自动在当前目录创建:
roomid=rid
snickMsg='16789'
LocalMsgTime=str(int(time.time()))
contentMsg='为什么超过长度了还能存进去1为什么超过长度了还能存进去2为什么超过长度了还能存进去3'

sqlTableName='TM'+LocalMsgTime+'RD'+roomid#+'@A'+LocalMsgTime+'.db'
conn = sqlite3.connect('tanmu.db')
cursor = conn.cursor()
strEx='create table '+sqlTableName+' (id int(10) primary key, name varchar(10), word varchar(50))'
cursor.execute(strEx)
idvalue=1
strEx='insert into '+sqlTableName+' (id, name, word) values ('+roomid+',\''+str(idvalue)+'\',\''+LocalMsgTime+'\')'
cursor.execute(strEx)
cursor.close()
conn.commit()
conn.close()

# 查询记录：
conn = sqlite3.connect('tanmu.db')
cursor = conn.cursor()
# 执行查询语句:
strEx='select * from '+sqlTableName+' where id=?'
print(strEx)
cursor.execute(strEx, roomid)
# 获得查询结果集:
values = cursor.fetchall()
print(values)
cursor.close()
conn.close()