#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import time
# 连接到SQLite数据库
# 数据库文件是test.db
# 如果文件不存在，会自动在当前目录创建:

snickMsg='16789'
LocalMsgTime=str(int(time.time()))
contentMsg='为什么超过长度了还能存进去1为什么超过长度了还能存进去2为什么超过长度了还能存进去3'

sqlTableName='TM'+sqlTime+'RD'+roomid#+'@A'+sqlTime+'.db'
print(sqlTableName)
conn = sqlite3.connect('tanmu.db')
# 创建一个Cursor:
cursor = conn.cursor()

# 执行一条SQL语句，创建user表:
strEx='create table '+sqlTableName+' (id int(2) primary key, name varchar(10), word varchar(20))'
#cursor.execute("create table user (id int(2) primary key, name varchar(10), word varchar(20))"%(sqlTableName))
print(strEx)
cursor.execute(strEx)

# 继续执行一条SQL语句，插入一条记录:
# idvalue=list()
# idvalue.append(12345)
# namevalue=list()
# namevalue.append(' sfdsflksjjghfjgkldjfldskjaf')
idvalue=1
strEx='insert into '+sqlTableName+' (id, name, word) values ('+roomid+',\''+str(idvalue)+'\',\''+sqlTime+'\')'
print(strEx)
cursor.execute(strEx)
#cursor.execute("insert into user (id, name, word) values ('%d','%s','%s')"%(sqlTableName, idvalue, namevalue,sqlTime))
# 通过rowcount获得插入的行数:
print('rowcount =', cursor.rowcount)
# 关闭Cursor:
cursor.close()
# 提交事务:
conn.commit()
# 关闭Connection:
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