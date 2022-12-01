"""
responder.py
Author: Madhukumar Seshadri
Copyright (c) Madhukumar Seshadri.
Purpose - find the responder for the request, make responder and return
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

class twresponder:
	""" talkweb responder .. use respondfor to get the responder .."""
	def respondusingmodule(self,appbasedir,module,environ,session=None,cookies=None):
		""" uri is the module name
			appbasedir is path of root app dir that will have reponder directory to have
			responders with ending slash
		"""
		responder = self.makeresponder(appbasedir,module,environ,session,cookies)
		return responder

	""" get responder module from router file"""
	def responderfromroutes(self,appbasedir,environ,router,session=None,cookies=None):
		#request_method = environ["REQUEST_METHOD"]
		#script_name = environ["SCRIPT_NAME"]
		#path_info = environ["PATH_INFO"]
		path = environ["PATH_INFO"]
		qs=environ["QUERY_STRING"]

		f = open(router,"r")
		
		for line in f.readlines():
			route,module = line.split()
			if re.search(route,path):
				return self.makeresponder(appbasedir,module,environ,session,cookies)
		
		return None

	""" get responder module from query string param r """
	def responderfor(self,appbasedir,environ,session=None,cookies=None):
		""" environ["QUERY_STRING"] is expected to be responder	"""
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

		uiresponder=self.makeresponder(appbasedir,module,environ,session,cookies)

		return uiresponder

	def makeresponder(self,appbasedir,module,environ,session=None,cookies=None):
		""" we make it only here so that it uniform """

		classname="myresponder"; instancename="this";
		otype="ui"
		if otype == "ui":
			mybase="uiresponder"
		else:
			mybase="responder"

		m=live(module,appbasedir+os.sep+'responders')
		if not m:
			print ("responder.py:live> couldn't load module:"+ m.__name__ + '\n')

		if classname not in m.__dict__:
			print ("responder.py:live> couldn't find class in " + str(m) +'\n')

		aninstance=type.__new__(m.__dict__[classname],instancename,(),{})

		if not aninstance:
			print (environ,"responder.py:live> couldn't instantiate :" + classname +'\n')
			return

		#qsaofa = http_transport.xtract_qs(qs)
		
		self.initresponder(aninstance,appbasedir,environ,session,cookies,module)
		return aninstance

	def initresponder(self,aresponder,appbasedir,environ=None,session=None,\
	                  cookies=None,module=""):
		""" only place a responder is initialized .. """
		aresponder.environ=environ
		aresponder.usession=session
		aresponder.cookies=cookies
		aresponder.appbasedir=appbasedir
		aresponder.formdata=None
		aresponder.module=module
		aresponder.qs=environ["QUERY_STRING"]


""" section app inheritables """
class responder(type):
	""" Others will become my descendant """
	__inheritances__=[type]

	def setsession(self,usession):
		self.usession = usession

	def setcookies(self,cookies):
		self.cookies = cookies

	def requestmethod(self):
		return self.environ["REQUEST"]
	
	def requestheader(self,k):
		return self.environ["HTTP_"+k.upper()]

	def urlscheme(self):
		return self.environ["wsgi.url_scheme"]

	def host(self):
		return self.environ["HTTP_HOST"]

	def servername(self):
		return self.environ["SERVER_NAME"]
	
	def serverport(self):
		return self.environ["SERVER_PORT"]

	def scriptname(self):
		return self.environ["SCRIPT_NAME"]

	def path(self):
		return self.environ["PATH_INFO"]

	def qs(self):
		return self.environ["QUERY_STRING"]

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
