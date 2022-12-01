"""
simpleresponder
filename is used to call from url with ?r=simpleresponder
Author: Madhukumar Seshadri
Copyright (c) Madhukumar Seshadri
"""
from talkback import *
from talkweb import *
import config

class myresponder(uiresponder):
	"""
		Inherited great - What's available for use?
		self.environ=environ
		#self.environ (mod_wsgi's environ variable)
		self.usession=session
		self.cookies=cookies
		#self.usession - if set in gate.py or passed
		#self.cookies - if set in gate.py or passed
		#if you are going to manage and session and cookies here, 
		#you can do that as well using session module
		self.appbasedir=appbasedir
		#basedir where gate.py was found
		self.formdata=None
		#use self.processform() to get self.formdata
		self.qs=qs
		#query string
		This simple responder was called with ?r=simpleresponder
	"""
	def respond(self):
		""" your response please """
		status = '200 OK'
		response_headers=[("Content-type","text/html;charset=utf-8;")]

		#print to apache log
		#print('an',an,'wan',wan,'abd',abd)

		fn = self.appbasedir + os.sep + 'html' + os.sep + "simpleresponse.html"
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
