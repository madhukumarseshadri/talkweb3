""" 
fskeeper.py
Author - Madhukumar Seshadri
Copyright (c) Madhukumar Seshadri
Purpose - File store for sessions 
"""

from pickle import *
from .app import *
from .path import *
import os

session_store_suffix=".store"

class fskeeper:
	""" filesystem keeper """
	def __init__(self,**kwargs):
		#self.request=req
		if 'basedir' not in kwargs:
			print("Need basedir to sessions store root") 
		self.basedir=kwargs['basedir']

	def getfile(self,sessionid):
		return self.basedir + os.sep + sessionid + session_store_suffix

	def getfrom(self,sessioncookie):
		""" input is sessioncookie identified by session object """
		return self.get(sessioncookie.value)

	def get(self,sessionid):
		""" input is sessionid """
		obj=None
		fn=self.getfile(sessionid)
		try:
			f=open(fn,"rb")
		except:
			return None
		
		obj=loads(f.read())
		f.close()
		return obj

	def put(self,s):
		""" where s is session object possibly created using session cookie"""
		fn=self.getfile(s.id)
		f=open(fn,"wb")
		f.write(dumps(s))
		f.close()

	def pop(self,s):
		""" where s is session object """
		# _@todo deleteincache
		fn=self.getfile(s.id)
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


		