"""
session.py
Author - Madhukumar Seshadri
keepers, keeper and payload - for session
	keepers give me a keeper
"""
import uuid
import os
from .cookie import *
from .app import *
from talksql import *
from pickle import *
from .path import *

_session_store_suffix=".store"

idgen=uuid.uuid1

class session:
	""" payload """
	def __init__(self,id=None,value={}):
		""" you can create this or you can get this from cookie """
		if not id:
			self.id=str(idgen())
		else:
			self.id=id
		self.store=value

	def __str__(self):
		""" string representation """
		return self.id + ":" + str(self.store)

class sqlsessionkeeper:
	""" session is stored in relational database """
	def __init__(self,cfg):
		#self.request=req
		self.conn=ipconnect(cfg)
	
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

class fskeeper:
	""" 	ask sessionkeepers akeeper for me and not directly
		  I store and retrieve sessions	"""
	def __init__(self,environ):
		#self.request=req
		self.environ=environ

	def getfile(self,sessionid):
		basedir = appbasedir(self.environ)
		sessionsroot = basedir + os.sep + "sessions"
		output=filesusingfilter(sessionsroot,sessionid)
		if len(output) < 1:
			print ("wsgitalkback:sessionid",sessionid,"did not qualify")
			#@todo cookie need to be told wipe off
			return ""
		return sessionsroot + os.sep + output[0][0]

	def getfrom(self,sessioncookie):
		""" input is sessioncookie identified by session object """
		return self.get(sessioncookie.value)

	def get(self,sessionid):
		""" input is sessionid """
		obj=None
		fn=self.getfile(sessionid)
		if not fn:
				return None
		try:
			f=open(fn,"r")
			s=f.read()
		except (IOError, e):
			print ("fskeeper",e)
		if s:
			obj=loads(s)
		f.close()
		return obj

	def put(self,s):
		""" where s is session object possibly created using session cookie"""
		fn=self.getfile(s.id)
		if not fn:
			print ("wsgitalkback:grave error session file cannot be found", sessionid)
		f=open(fn,"w")
		x=dumps(s)
		f.write(x)
		f.close()

	def pop(self,s):
		""" where s is session object """
		# _@todo deleteincache
		fn=self.getfile(s.id)
		if not fn:
			print ("wsgitalkback:grave error session file cannot be found", sessionid)
		os.remove(fn)

	def new(self,sci):
		""" returns a new session """
		basedir = appbasedir(self.environ)
		sessionsroot = basedir + os.sep + "sessions"
		asession = session(sci)

		#create sessions directory if not exists
		f = open(sessionsroot + os.sep + asession.id,"w")
		self.put(asession)
		f.close()

		return asession

	def persist(self,usession):
		self.put(usession)

	def invalidate(self,usession):
		usession.store={}
		self.pop(usession)



""" Template do not erase inherit ..
class sessionkeeper:
	# 	ask sessionkeepers akeeper for me and not directly
	#	  I store and retrieve sessions
	def __init__(self,environ):
		#self.request=req
		self.filepath=appbasedir(environ) + "/" + appname(environ) + _session_store_suffix
		self.mystore=filestore
		#self.replicator=replication service to replicate values to others
		#self.mycache = "__not_available__"

	def getfrom(self,sessioncookie):
		#input is sessioncookie identified by session object
		return self.mystore.get(sessioncookie.value,self.filepath)3

	def get(self,sessionid):
		# input is sessionid
		return self.mystore.get(sessionid,self.filepath)

	def put(self,s):
		# where s is session object possibly created using session cookie
		# _@todo retrievefromcache and updatecache
		#self.mystore.pop(s.key,self.store)
		self.mystore.put(s,s.id,self.filepath)

	def pop(self,s):
		#where s is session object
		# _@todo deleteincache
		return self.mystore.pop(s.id,self.filepath)

	def new(self,xsession=None):
		#returns a new session
		if xsession is None:
			asession = session()
		else:
			asession=xsession
		self.put(asession)
		return asession

	def persist(self,usession):
		self.put(usession)

	def invalidate(self,usession):
		usession.store={}
		self.pop(usession)
"""
