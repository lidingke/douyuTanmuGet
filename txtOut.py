import sqlite3
import time
import re
import sys

IDdict={'10091':'囚徒','10029':'王师傅','31131':'SOL君','10027':'瓦莉拉','10025':'冰蓝飞狐','10003':'星妈'}

def data(timeStart,roomid,tableStr):
	conn = sqlite3.connect('pandadanmu.db')
	cursor = conn.cursor()
	strEx='select * from '+tableStr
	cursor.execute(strEx)
	values = cursor.fetchall()
	cursor.close()
	conn.close()
	if not IDdict.get(roomid):
		IDdict[roomid]=roomid
	txtName=timeStart+'日'+IDdict[roomid]+'弹幕汇总.txt'

	if values:
		writefile=open(txtName,"w")
		print('生成：',txtName)
		for v in values:
			writefile.writelines([time.ctime(v[0])[4:19],':',v[1],':',v[2],'\n'])
		writefile.close()



def main(date):
	con = sqlite3.connect('pandadanmu.db')
	cursor = con.cursor()
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tableLst=cursor.fetchall()
	cursor.close()
	con.close()
	localTime=time.localtime()
	tyear=str(localTime.tm_year)
	tmoon=str(localTime.tm_mon) if len(str(localTime.tm_mon))==2 else '0'+str(localTime.tm_mon)
	tday=str(localTime.tm_mday) if len(str(localTime.tm_mday))==2 else '0'+str(localTime.tm_mday)
	dateNow=tyear+tmoon+tday
	date=dateNow if date=='-1' else date
	print(date)
	for table in tableLst:
		tableStr=''.join(table)
		timeStart=tableStr.split('RD')[0].split('TM')[1]
		roomid=tableStr.split('RD')[1]
		#print(timeStart)
		if timeStart == date:
			#print(ctime,':',tableStr)
			data(timeStart,roomid,tableStr)



if __name__=='__main__':
	date= sys.argv[1] if len(sys.argv)>1 else '-1'
	print(date)
	main(date)

#python3 txtOut.py 20160220

