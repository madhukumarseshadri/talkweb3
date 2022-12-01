"""
Author - Madhukumar Seshadri
Copyright(c) Madhukumar Seshadri
A wrapper to mysqlconnector sockconnect need to be moved application layer
todo: multi=true in execute yet to be done
ipcfg and cfg need to come from application
"""
from mysql import connector
import time

ipcfg = {
    'user': '',
    'password': '',
    'host': '',
	'db':'' }

cfg = { 'socket':"/tmp/mysql.sock",
    'user': '',
    'password': '',
    'host': '127.0.0.1',
	'db':'' }

def sockconnect(cfg):
	""" connect via socket """
	try:
		conn = connector.Connect(unix_socket=cfg['socket'],user=cfg['user'],passwd=cfg['password'])
	except (connector.errors.InterfaceError, e):
		print("couldn't connect to database using ",socket,user,passwd)
		return
	#print "connection .. "
	#for akey in conn.__dict__:
		#print akey,":",conn.__dict__[akey]
	if 'db' in cfg:
		conn.cmd_init_db(cfg['db'])
	return conn

def ipconnect(ipcfg):
	""" connect using network - not done """
	try:
		conn = connector.Connect(**ipcfg)
	except connector.errors.InterfaceError as e:
		print ("couldn't connect to database using ",socket,user,passwd)
		return
	if 'db' in ipcfg:
		conn.cmd_init_db(ipcfg['db'])
	return conn

def use(conn,db):
	#print "connection user is ",conn._user
	conn.cmd_init_db(db)

def xec(conn,s,data=None):
	""" conn is our connection object and is is statement commits use connector api
		if you want to manage commits and rollbacks """
	c = conn.cursor()
	c.execute(s,data)
	conn.commit()
	return c

def xecm(conn,s,data):
	""" for datainserts data can be tuple or dict """
	c = conn.cursor()
	c.executemany(s,data)
	conn.commit()
	return c

##-- resultset is aofa
##-- @add-feature I need actual datatypes in rs and column names in a set with order
def xecrs(conn,s,data=None):
	rs=[]
	ic=0
	c = conn.cursor()
	c.execute(s,data)
	for i in c:
		rs.append([])
		for j in range(len(i)):
			rs[ic].append(i[j])
		ic += 1
	c.close()
	return (rs,c)

def xecmrs(conn,s,data=None):
	"""
	:param conn:result of sockconnect or ipconnect
	:param s: sql
	:param data:data for sql
	:return: resultset as [[]] and cursor object associated with it
	do not use as cursor object of last resultset will be given out
	"""
	rs=[]
	c = conn.cursor()
	for result in c.execute(s,data,True):
		if result.with_rows:
			rs.append((result.fetchall(),result))
		else:
			rs.append(([],result))
	c.close()
	return rs

def xecrsd(conn,s,cols=[],data=None):
	rs=[]
	ic=0
	c = conn.cursor()
	c.execute(s,data)
	for i in c:
		rs.append({})
		for j in range(len(i)):
			rs[ic][cols[j]]=i[j]
		ic += 1
	c.close()
	return (rs,c)


##-- @add-feature column names as a set with order, if given
def xecr(conn,s):
	rs={}
	c = conn.cursor()
	c.execute(s)
	for i,k in enumerate(c):
		#print i,k
		rs[i]=[]
		for j in range(len(k)):
			rs[i].append(k[j])
	c.close()
	return rs

##-- transpose a resultset
def transpose(rs,rangeofcols):
	output = []
	for i in rangeofcols:
		output.append([])
	for ri,r in enumerate(rs):
		for ci,c in enumerate(r):
			if ci in rangeofcols:
				output[ci].append(rs[ri][ci])
	return output

##--send time
def strof(t):
	return time.strftime("%Y-%m-%d %H:%M:%S",t)

##-- to time
def timeof(s):
	return time.strptime(s,"%Y-%m-%d %H:%M:%S")

##-- expand dict of keys to have value array's of dictionary
def addkeyasfirstcellof(x):
	for akey in x:
		clonedset = []
		clonedset.append(akey)
		for anelement in x[akey]:
			clonedset.append(anelement)
		x[akey]=clonedset
	return x

##-- insert for values in a dictionary {{}..}
def sqlofd(values,table,cols,addcol=[],sameval=[]):
	cols = cols.split(",")
	psql = "insert into " + table + "("
	sql=""
	for i in cols:
		psql = psql + i.strip() + ","
	if len(addcol) > 0:
		for i in range(len(addcol)):
			psql = psql + addcol[i] + ","
	psql = psql[0:len(sql)-1]
	psql = psql + ") values ("

	for i in values.keys():
		sql = sql + psql
		for j in range(len(cols)):
			if j < len(values[i]):
				x = str(values[i][j])			##-this is cell's value
			else:
				x = ""
			sql = sql + '"' +  x.replace('"','\\"')  + '"' + ","
		if len(addcol) > 0:
			for i in range(len(addcol)):
				sql = sql + '"'  + sameval[i] + '"' + ","
		sql = sql [0:len(sql)-1] + ");\n"
	return sql


##-- insert for values in aofa [[]..]
def sqlofa(values,table,cols,addcol=[],sameval=[]):
	cols = cols.split(",")
	psql = "insert into " + table + "("
	sql=""
	for i in cols:
		psql = psql + i.strip() + ","
	if len(addcol) > 0:
		for i in range(len(addcol)):
			psql = psql + addcol[i] + ","
	psql = psql[0:len(sql)-1]
	psql = psql + ") values ("

	for i in values:
		sql = sql + psql
		for j in range(len(cols)):
			if j < len(i):
				x = str(i[j])			##-- final cell's value
			else:
				x = ""
			if x == "NULL":
				sql = sql + x + ","
			else:
				sql = sql + '"' +  x.replace('"','\\"')  + '"' + ","
		if len(addcol) > 0:
			for i in range(len(addcol)):
				sql = sql + '"'  + sameval[i] + '"' + ","
		sql = sql [0:len(sql)-1] + ");\n"
	return sql


##-- wrapper for both dict and array
def sqlof(values,table,cols,addcol=[],sameval=[]):
	sql=""
	if type(values) is dict:
		sql = sqlofd(values,table,cols,addcol,sameval)
	elif type(values) is list:
		sql = sqlofa(values,table,cols,addcol,sameval)
	else:
		print ("error:unsupported value type sqli:insert - values must be a dict or array")
	return sql

##-- generates and fire sqls-rapid succession or in one shot
def insert(conn,values,table,cols,addcol=[],sameval=[],oneshot=0):
	sql = sqlof(values,table,cols,addcol,sameval)
	if oneshot:
		xecm(conn,sql)
	else:
		sqll = sql.split(";")
		for i in sqll:
			i = i.strip()
			print (">"+i)
			xec(conn,i)

def xsqlofa(values,table,cols,addcol=[],sameval=[]):
	""" returns operation and values for cursor.execute """
	cols = cols.split(",")
	psql = "insert into " + table + "("
	sql=""
	params=[]
	for i in cols:
		psql = psql + i.strip() + ","
	if len(addcol) > 0:
		for i in range(len(addcol)):
			psql = psql + addcol[i] + ","
	psql = psql[0:-1]
	psql = psql + ") values ("

	for j in range(len(cols)):
		x = "%s"
		sql = sql + '"' +  x  + '"' + ","

	sql = psql + sql [0:-1] + ")"

	for i in values:
		for j in range(len(cols)):
			if j < len(i):
				x = str(i[j])			##-- final cell's value
			else:
				x=""
			params.append(x)
		if len(addcol) > 0:
			for i in range(len(addcol)):
				params.append(sameval[i])

		#print sql
	return (sql,params)

import sys

if __name__ == "__main__":
	print ("testing sockconnect")
	conn = sockconnect(db="trans")

	print ("switching db to trans .. ")
	use(conn,"trans")

	print ("testing execute single ..creating temp table tmp")
	xec(conn,"create table if not exists tmp (x int, y float, z varchar(20), a binary)")

	print ("inserting into tmp ")
	xec(conn,'insert into tmp(x,y,z,a) values (1,2,"hello",2342352)')

	print ("testing xecrs ..  ")
	print (xecrs(conn,"select * from tmp"))

	print ("testing xecr ..  ")
	print (xecr(conn,"select * from tmp"))

	print ("testing xecm ..  ")
	print (xecm(conn,\
		'insert into tmp(x,y,z,a)	values (1,2,"hello",2342352);\
		 insert into tmp(x,y,z,a) values (1,2,"hello",2342352);'))

	print ("testing sqlof ..")
	values=[]
	values.append([]);
	values[0].append("00")
	values[0].append("02")
	print (sqlof(values,"users","anuser,username,pwd"))

	print ("testing sqlof ..")
	values={}
	values[0]=[]
	values[0].append("00")
	values[0].append("01")
	print (sqlof(values,"users","anuser,username,pwd"))

	print ("testing xsqlofa ..")
	values=[]
	values.append([]);
	values[0].append("00")
	values[0].append("01")
	print (xsqlofa(values,"users","anuser,username,pwd"))

	print ("cleaning up ..  ")
	xec(conn,'drop table tmp')

	conn.close()
	#"select"

"""
c.cursor().execute("insert into users(anuser,name,pwd,email,enctype) values (%s,%s,%s,%s,%s);
insert into userquestions(aquestion,ananswer,anuser) values (%s,%s,%s)",("adfsfas","adsffas","adfasfda","adfas","Asdfasd","asdfas","adfas","asdfasdas"),multi=True)
not sure whether this executes across many updates or inserts
"""
