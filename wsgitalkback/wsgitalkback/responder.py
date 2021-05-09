"""
responder.py
Author: Madhukumar Seshadri
Copyright (c) Madhukumar Seshadri.
Purpose - find the responder for the request and respond
"""
from .app import *
from .transport import *
from .formdata import *
from .loader import *
import re
import os

class responders:
	""" factory .. ask me for uriresponder class .. """
	@classmethod
	def uriresponder(cls):
		return twresponder()

	@classmethod
	def frommodule(cls,modulename,rootdir):
		urlresponder=twresponder()
		aresponder=urlresponder.makeresponder(modulename,rootdir)
		return aresponder

class twresponder:
	""" talkweb responder .. use respondfor to get the responder .."""
	def respondusingmodule(self,uri,environ,session=None,cookies=None):
		""" uri is the module name """
		rootdir=appbasedir(environ)
		responder = self.makeresponder(uri,rootdir,environ,session,cookies)
		return responder

	def respondfor(self,environ,session=None,cookies=None):
		""" environ["QUERY_STRING"] is expected to be responder	"""
		rootdir=appbasedir(environ)
		qs=environ["QUERY_STRING"]
		#print('type(qs)',type(qs))

		qsaofa = http_transport.xtract_qs(qs)

		module=""
		if len(qsaofa) > 0:
			if len(qsaofa[0]) > 1:
				if qsaofa[0][0] == 'r':
					module = qsaofa[0][1]

		if not module:
			return None

		if not module:
			print ('responder.py:twresponder:respondfor> no module for' +\
				 environ.args + "\n")
			return

		uiresponder=self.makeresponder(module,rootdir,environ,session,cookies,qs,qsaofa)
		#if uiresponder:
			#uiresponder.p = page(uiresponder.__name__)

		return uiresponder

	def makeresponder(self,module,rootdir,environ=None,session=None,cookies=None,qs="",qsaofa=[]):
		""" we make it only here so that it uniform """

		sys.path.append(rootdir + appname(environ))
		sys.path.append(rootdir + appname(environ) + os.sep + "responders")

		classname="myresponder"; instancename="thisresponder";
		otype="ui"
		if otype == "ui":
			mybase="uiresponder"
		else:
			mybase="responder"

		m=live(module,rootdir+'/responders')
		if not m:
			print ("responder.py:live> couldn't load module:"+ m.__name__ + '\n')

		if classname not in m.__dict__:
			print (self.environ,"responder.py:live> couldn't find class in " + str(m) +'\n')

		aninstance=type.__new__(m.__dict__[classname],instancename,(),{})

		if not aninstance:
			print (self.environ,"responder.py:live> couldn't instantiate :" + classname +'\n')
			return

		self.initresponder(aninstance,environ,session,cookies,rootdir,module,qs,qsaofa)
		return aninstance

	def initresponder(self,aresponder,environ=None,session=None,\
	                  cookies=None,appbasedir=None,module="",qs="",qsaofa=[]):
		""" only place a responder is initialized .. """
		aresponder.environ=environ
		aresponder.usession=session
		aresponder.cookies=cookies
		aresponder.appbasedir=appbasedir
		aresponder.formdata=None
		aresponder.module=module
		aresponder.qs=qs
		aresponder.qsaofa=qsaofa


""" section app inheritables """
class responder(type):
	""" Others will become my descendant """
	__inheritances__=[type]

	def setsession(self,usession):
		self.usession = usession

	def setcookies(self,cookies):
		self.cookies = cookies
	
	def requestheader(self,k):
		return self.environ["HTTP_"+k.upper()]

	def processform(self,encoding="utf-8"):
		""" process any get or posted """
		self.formdata=formdata.fromrequest(self.environ,encoding)

	def processinput(self):
		""" serialized bytes via ajax """
		incoming = self.environ["wsgi.input"]
		#mod_wsgi - either to use content-length or read in blocks
		octet=b''
		inp = incoming.read(1024*1024)
		while inp:
			octet += inp
			inp = incoming.read(1024*1024)
		return octet

	def respond(self):
		""" if you don't respond, what is point of being a responder """
		return "__meta__"

class uiresponder(responder):
	""" ui responder	"""
	__inheritances__=[responder]

	def respond(self):
		""" meat and potato of your code by overriding """
		#writeable.write(p.tohtml())
		return
