""" 
dbkeeper.py
Author - Madhukumar Seshadri
Copyright (c) Madhukumar Seshadri
Purpose - Db store for sessions. Needs the following session table in db
CREATE TABLE session (
  sessionid varchar(100) NOT NULL,
  obj blob,
  appname varchar(20) DEFAULT NULL,
  login tinyint(4) DEFAULT NULL,
  lastused datetime DEFAULT NULL
)
"""

from talksql import *
from pickle import *

class sqlsessionkeeper:
	""" session is stored in relational database """
	def __init__(self,**kwargs):
		#self.request=req
		if 'connection' not in kwargs:
			print('Need db connection to keep sessions. Db should have session table.')
		self.conn=kwargs['connection']
	
	def exists(self,sid):
		sql = "select sessionid from session where sessionid=%s"
		data = (sid,)
		rs,c=xecrs(self.conn,sql,data)
		if len(rs) > 0:
			return True
		else:
			return False

	def get(self,sid):
		#input is sessionid
		#print("wsgitalkback:get")
		sql = 'select obj from session where sessionid=%s'
		data=(sid,)
		rs,c=xecrs(self.conn,sql,data)
		obj=None
		if len(rs) > 0:
			if rs[0][0]:
				obj=loads(rs[0][0])
		return obj

	def put(self,s):
		""" where s is session object or string incase app wants to encrypt what it stores"""
		if self.exists(s.id):
			#print("performing update..")
			sql="update session set obj = %s where sessionid = %s"
			data=(dumps(s),s.id,)
			xec(self.conn,sql,data)
		else:
			#print("performing insert..")
			sql ='insert into session (sessionid, obj) values (%s,%s)'
			data = (s.id,dumps(s),)
			xec(self.conn,sql,data)

	def pop(self,s):
		""" where s is session object """
		#print("wsgitalback:del")
		sql = 'delete from session where sessionid =%s'
		data = (s.id,)
		xec(self.conn,sql,data)
	
	def popusingsid(self,sid):
		""" where s is session object """
		sql = 'delete from session where sessionid =%s'
		data = (sid,)
		xec(self.conn,sql,data)

	def new(self,sid):
		sql = 'insert into session (sessionid) values (%s)'
		data = (sid,)
		xec(self.conn,sql,data)
		return session(sid)
