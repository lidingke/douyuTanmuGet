sockStr=b'w\x01\x00\x00w\x01\x00\x00\xb2\x02\x00\x00type@=msgrepeaterlist/rid@=16789/lis\
t@=id@AA=75701@ASnr@AA=1@ASml@AA=10000@ASip@AA=danmu.douyutv.com@ASport@AA=12601\
@AS@Sid@AA=75702@ASnr@AA=1@ASml@AA=10000@ASip@AA=danmu.douyutv.com@ASport@AA=126\
02@AS@Sid@AA=74004@ASnr@AA=1@ASml@AA=10000@ASip@AA=danmu.douyutv.com@ASport@AA=8\
602@AS@Sid@AA=74003@ASnr@AA=1@ASml@AA=10000@ASip@AA=danmu.douyutv.com@ASport@AA=\
8601@AS@S/\x00/\x00\x00\x00/\x00\x00\x00\xb2\x02\x00\x00type@=setmsggroup/rid@=1\
6789/gid@=169/\x00"\x00\x00\x00"\x00\x00\x00\xb2\x02\x00\x00type@=scl/cd@=0/maxl\
@=30/\x008\x00\x00\x008\x00\x00\x00\xb2\x02\x00\x00type@=initcl/uid@=1305506713/\
cd@=6000/maxl@=30/\x00\x9f\x00\x00\x00\x9f\x00\x00\x00\xb2\x02\x00\x00type@=memb\
erinfores/silver@=0/gold@=0/strength@=0/weight@=300633515/exp@=0/curr_exp@=0/lev\
el@=1/up_need@=1000/fans_count@=636109/fl@=0/list@=/glist@=/\x00K\x00\x00\x00K\x00\x00\x00\xb2\x02\x00\x00rid@=16789/gid@=0/type@=bcrp/pt@=2/pid@=10165/pps@=9107100/rps@=0/\x00'

chatmsg=b'U\x01\x00\x00U\x01\x00\x00\xb2\x02\x00\x00type@=chatmessage/rescode@=0/sender@\
=14761178/content@=\xe6\x88\x91\xe7\x9a\x84\xe6\x98\xbe\xe5\x8d\xa1/snick@=\xe6\x82\
\x94\xe5\x88\x9d\xe8\xb0\x8ei/cd@=4/maxl@=22/chatmsgid@=e56c175b158649e558b51\d0000000000\
/col@=0/ct@=0/gid@=6/rid@=284584/sui@=id@A=14761178@Snick@A=\xe6\x82\x94\
\xe5\x88\x9d\xe8\xb0\x8ei@Srg@A=1@Spg@A=1@Sstrength@A=11120@Sver@A=20150929@S\
m_deserve_lev@A=0@Scq_cnt@A=0@Sbest_dlev@A=0@Slevel@A=8@Sgt@A=0@S/\x00'
#悔初谎i:我的显卡

import re

#def chatmsgGet(chatmsg):
if chatmsg.find(b'chatmessage'):
	contentMsg=b''.join(re.findall(b'content@=(.*?)/',chatmsg))
	snickMsg=b''.join(re.findall(b'@Snick@A=(.*?)@',chatmsg))
	print('hello')
	print(snickMsg.decode('utf-8'),':',contentMsg.decode('utf-8'))

# def danmuIpNPortGet():
# 	contextList=sockStr.split(b'\x00"')[0].split(b'\xb2\x02')

	# for cl in contextList:
	# 	tanmuIpNport=dict()
	# 	cl=cl.decode('utf-8','.ignore')
	# 	if cl.find('msgrepeaterlist'):
	# 		clstr=''.join(re.findall('list@=(.*?)/',cl))

	# 		for ls in clstr.split('@S'):
	# 			tanmuIp=''.join(re.findall('Sip@AA=(.*?)@',ls))
	# 			tanmuPort=''.join(re.findall('Sport@AA=(\d+)',ls))
	# 			tanmuIpNport[tanmuPort]=tanmuIp
	# 			print(tanmuIp,tanmuPort)
	# 	if cl.find('setmsggroup'):
	# 		tanmuIpNport['gid']=re.findall('gid@=(\d+)/',cl)
	# 		tanmuIpNport['rid']=re.findall('rid@=(.*?)/',cl)
	# return tanmuIpNport

	# for k,v in tanmuIpNport.items():
	# 	print(k,v)
	




