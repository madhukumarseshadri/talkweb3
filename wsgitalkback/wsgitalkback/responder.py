"""
 responder.py
 Purpose - find the responder for the request and respond
 Copyright (c) Madhukumar Seshadri. All rights reserved.
 See end of file for commentary, history and other details ..
 Introducing changes on April 10th 2014 ..

"""
from talkweb import *
from .app import *
from .headers import *
from .formdata import *
from .loader import *
import re
import os

class twserver:
	def __init__(self,environ,path,fn,traverse=0):
		self.environ=environ
		self.path=path
		self.fn=self.path + os.sep + "html" + os.sep + fn

	def respond(self):
		x=""
		#logthis(self.environ,"responder.py:twserver:respond>" + self.fn + "\n")
		try:
			#x=tohtml(self.fn)
			x=h2oo(self.fn)
		except IOError as e:
			logthis(self.environ,"a file by name " + self.fn + " could not be opened" + str(e) + "\n")
			pass
		return ('',[],x)

class responders:
	""" factory .. ask me for uriresponder class .. """
	@classmethod
	def uriresponder(cls):
		return twresponder()

	@classmethod
	def frommodule(cls,modulename,rootdir):
		urlresponder=twresponder()
		aresponder=urlresponder.makeresponder(modulename,rootdir)
		if aresponder:
			return aresponder
		return

class twresponder:
	""" talkweb responder .. use respondfor to get the responder .."""
	def respondusingmodule(self,uri,environ,session=None,cookies=None):
		""" uri is the module name """
		rootdir=appbasedir(environ)
		responder = self.makeresponder(uri,rootdir,environ,session,cookies)
		#responder.p = page(responder.__name__)
		return responder

	def respondfor(self,environ,session=None,cookies=None):
		""" environ["QUERY_STRING"] is expected to be responder	"""
		#logthis(environ,"responder.py:twresponder:responderfor")
		rootdir=appbasedir(environ)
		qs=environ["QUERY_STRING"]

		qsaofa = html_transport.xtract_qs(qs)

		module=""
		if len(qsaofa) > 0:
			if len(qsaofa[0]) > 1:
				if qsaofa[0][0] == 'r':
					module = qsaofa[0][1]

		if not module:
			return None

		if module[-3:] == ".tw":
			path=appbasedir(environ)
			#logthis(environ,"looking for twserver")
			return twserver(environ,path,module)

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

		sys.path.append(rootdir + os.sep + appname(environ))
		sys.path.append(rootdir + os.sep + appname(environ) + os.sep + "responders")

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
	
	def requestheaders(self,k):
		return self.environ["HTTP_"+k.upper()]

	def processforms(self):
		""" process any posted forms in the environuest """
		if not self.environ:
			#logtowebserver error log or syslog
			return
		self.formdata=formdata.fromrequest(self.environ)

	def respond(self,writeable):
		""" if you don't respond, what is point of being a responder """
		return "__meta__"

class uiresponder(responder):
	""" ui responder	"""
	__inheritances__=[responder]

	def respond(self):
		""" meat and potato of your code by overriding """
		#writeable.write(p.tohtml())
		return
