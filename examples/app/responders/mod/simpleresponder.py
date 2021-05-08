"""
simple responder
This simple responder can be called with ?r=mod/simpleresponder
Author: Madhukumar Seshadri
Copyright (c) Madhukumar Seshadri
"""
from wsgitalkback import *
from talkweb import *
import config

class myresponder(uiresponder):
	""" your response """
	def respond(self):
		""" your response please """
		status = '200 OK'
		response_headers=[]

		#application name
		an = appname(self.environ)
		#wsgi alias for application configured in apache conf
		wan = wsgialias(self.environ)
		#application base directory
		abd = appbasedir(self.environ)

		#print to apache log
		#print('an',an,'wan',wan,'abd',abd)

		fn = abd + 'html' + os.sep + "simpleresponse.html"
		#come to object (cells) from html file
		page=h2oo(fn)
		#find the hello world container cell within the page
		hwc=page.findcellbyid("response")
		#add hello world cell from string by adding 's' to h2oo (html to object)
		hwc.addcell(h2oo("<div>Dumping mod_wsgi's environ</div>",'s'))
		
		self.environ["SERVER_SOFTWARE"]=""

		for k in self.environ:
			s = """<div>
			<div style="display:inline-block;border: solid 1px red;">%s</div>
			<div style="display:inline-block;border: solid 1px red;">%s</div>
			<div style="display:inline-block;border: solid 1px red;">%s</div>
			<div>
			""" %(k,str(self.environ[k]),str(type(self.environ[k]))[1:-1])
			hwc.addcell(h2oo(s,'s'))

		#return these to gate.py
		return (status,response_headers,page.html())
