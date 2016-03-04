import re
msgrepeaterlist=b'w\x01\x00\x00w\x01\x00\x00\xb2\x02\x00\x00type@=msgrepeaterlist/rid@=16789/lis\
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

chatmessage=b'U\x01\x00\x00U\x01\x00\x00\xb2\x02\x00\x00type@=chatmessage/rescode@=0/sender@\
=14761178/content@=\xe6\x88\x91\xe7\x9a\x84\xe6\x98\xbe\xe5\x8d\xa1/snick@=\xe6\x82\
\x94\xe5\x88\x9d\xe8\xb0\x8ei/cd@=4/maxl@=22/chatmsgid@=e56c175b158649e558b51\d0000000000\
/col@=0/ct@=0/gid@=6/rid@=284584/sui@=id@A=14761178@Snick@A=\xe6\x82\x94\
\xe5\x88\x9d\xe8\xb0\x8ei@Srg@A=1@Spg@A=1@Sstrength@A=11120@Sver@A=20150929@S\
m_deserve_lev@A=0@Scq_cnt@A=0@Sbest_dlev@A=0@Slevel@A=8@Sgt@A=0@S/\x00'
#content@=弹幕内容，sinck@=昵称

userrnter=b'`\x01\x00\x00`\x01\x00\x00\xb2\x02\x00\x00type@=userenter/rid@=16789/gid@=194/\
userinfo@=id@A=27051443@Sname@A=qq_Qq5dQ9et@Snick@A=\xe8\x91\xa3\xe5\xb0\x8f\xe5\
\xa4\xab\xe4\xb8\xab@Srg@A=1@Spg@A=1@Srt@A=1445778191@Sbg@A=0@Sweight@A=0@Sstren\
gth@A=6500@Scps_id@A=0@Sps@A=1@Sver@A=20150331@Sm_deserve_lev@A=3@Scq_cnt@A=1@Sb\
est_dlev@A=3@Sglobal_ban_lev@A=0@Sexp@A=188100@Slevel@A=9@Scurr_exp@A=26100@Sup_\
need@A=40400@Sgt@A=0@S/\x00'

dgn=b'\xcd\x00\x00\x00\xcd\x00\x00\x00\xb2\x02\x00\x00type@=dgn/gfid@=104/gs@=1/gfcn\
t@=1/hits@=1/sid@=2564049/src_ncnm@=\xe5\x9d\x8f\xe5\xbf\x83\xe8\x82\xa0\xe7\x9a\
\x84\xe6\xa9\x98\xe5\xad\x90/rid@=16789/gid@=194/lev@=0/cnt@=0/sth@=64660/level@\
=6/bdl@=0/dw@=301053615/rpid@=0/slt@=0/elt@=0/srg@=1/spg@=1/\x00'

upgrade=b'P\x00\x00\x00P\x00\x00\x00\xb2\x02\x00\x00type@=upgrade/uid@=16659562/rid@=167\
89/gid@=194/nn@=sleep4007/level@=4/\x00'

keeplive=b'3\x00\x00\x003\x00\x00\x00\xb2\x02\x00\x00type@=keeplive/tick@=1455420838/uc@=32697/\x00'

donateres=b'\xef\x00\x00\x00\xef\x00\x00\x00\xb2\x02\x00\x00type@=donateres/rid@=16789/gid\
@=194/ms@=100/sb@=12861/src_strength@=17400/dst_weight@=301060515/hc@=4/r@=0/gfi\
d@=1/gfcnt@=0/sui@=id@A=3577140@Srg@A=1@Snick@A=\xe7\x81\xaf\xe5\xa1\x94\xe4\xbc/\x00'

donateres1=b'\xe2\x00\x00\x00\xe2\x00\x00\x00\xb2\x02\x00\x00type@=donateres/rid@=25515/gid\
@=312/ms@=100/sb@=17/src_strength@=700/dst_weight@=199511153/hc@=1/r@=0/gfid@=1/\
gfcnt@=0/sui@=id@A=38034385@Srg@A=1@Snick@A=447802922@Scur_lev@A=0@Scq_cnt@A=0@S\
best_dlev@A=0@Slevel@A=2@S/\x00'
#dst_weight@=体重

bc_buy_deserve=b'\x97\x01\x00\x00\x97\x01\x00\x00\xb2\x02\x00\x00type@=bc_buy_deserve/level@=9/\
lev@=3/rid@=16789/gid@=194/cnt@=1/hits@=1/sid@=27072146/sui@=id@A=27072146@Sname\
@A=auto_l1AafOnuG6@Snick@A=\xe5\x8d\x88\xe5\xa4\x9c\xe4\xb8\xb6Slaughter@Srg@A=1\
@Spg@A=1@Srt@A=1445793083@Sbg@A=0@Sweight@A=0@Sstrength@A=3900@Scps_id@A=0@Sps@A\
=1@Sver@A=20150929@Sm_deserve_lev@A=0@Scq_cnt@A=0@Sbest_dlev@A=0@Sglobal_ban_lev\
@A=0@Sexp@A=193500@Slevel@A=9@Scurr_exp@A=31500@Sup_need@A=35000@Sgt@A=0@S/\x00'

onlinegift=b'l\x00\x00\x00l\x00\x00\x00\xb2\x02\x00\x00type@=onlinegift/rid@=16789/uid@=216\
25213/gid@=194/sil@=130/if@=6/ct@=0/nn@=\xe4\xba\x91\xe5\xb8\x95/ur@=1/level@=10\
/\x00'


lst=chatmsg.split(b'\xb2\x02')
for x in lst:
	print(x)
#def chatmsgGet(chatmsg):
# if chatmsg.find(b'chatmessage'):
# 	contentMsg=b''.join(re.findall(b'content@=(.*?)/',chatmsg))
# 	snickMsg=b''.join(re.findall(b'@Snick@A=(.*?)@',chatmsg))
# 	print(snickMsg.decode('utf-8'),':',contentMsg.decode('utf-8'))
#def danmuIpNPortGet():

# print(re.findall(b'content@=(.*?)/',chatmsg))
# content=re.search(b'content@=(.*?)/',chatmsg)
# if content:
# 	print(content.group(1))

# content=re.search(b'content@=(.*?)/',onlinegift)
# if content:
# 	print(content)
# contextList=sockStr.split(b'\x00"')[0].split(b'\xb2\x02')
# tanmuIpNport=dict()
# for cl in contextList:

# 	cl=cl.decode('utf-8','.ignore')
# 	#print(cl,len(cl))
# 	if re.search('msgrepeaterlist',cl):
# 		tanmuIpNport['add']=re.findall('Sip@AA=(.*?)@',cl)
# 		tanmuIpNport['port']=re.findall('Sport@AA=(\d+)',cl)
# 		#tanmuIpNport[tanmuPort]=tanmuIp
# 		print('msgrepeaterlist')
# 		#print(tanmuIp[-1],tanmuPort[-1])
# 	elif re.search('setmsggroup',cl):
# 		tanmuIpNport['gid']=re.findall('gid@=(\d+)/',cl)
# 		tanmuIpNport['rid']=re.findall('rid@=(.*?)/',cl)
# 		print('setmsggroup')

# 	#print(tanmuIp,tanmuPort)
# #return tanmuIpNport
# for k,v in tanmuIpNport.items():
# 	print(k,v)

# print(tanmuIpNport.get('port')[0])

	




