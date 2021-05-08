"""
session.py
Author - Madhukumar Seshadri
Copyright(c) Madhukumar Seshadri
"""
import uuid
import os
from .cookie import *
from .app import *
from .path import *

idgen=uuid.uuid1

class session:
	""" payload """
	def __init__(self,id=None,value={}):
		""" creation id if none, generated if given, set
			value is dict payload for session id
		"""
		if not id:
			self.id=str(idgen())
		else:
			self.id=id
		self.store=value

	def __str__(self):
		""" string representation """
		return self.id + ":" + str(self.store)


""" 
Interface do not erase inherit  ..
this can be made as inteface and inherited ..

class sessionkeeper:
	def __init__(self,**kwargs):
		#kwargs to init
		pass

	def getfrom(self,sessioncookie):
		pass
	
	def get(self,sessionid):
		pass

	def put(self,s):
		#s is session object
		pass

	def pop(self,s):
		#s is session object
		pass

	def new(self,s):
		#s is session object
		pass

	def persist(self,s):
		#s is session object
		self.put(usession)
"""
