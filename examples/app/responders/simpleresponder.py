"""
myresponder
filename is used to call from url
all responders are myresponders if you did not notice
Copyright (c) Madhukumar Seshadri
"""
from wsgitalkback import *
from talkweb import *

class myresponder(uiresponder):
	"""
		self.usession
		self.cookies
		self.environ (mod_wsgi's environ variable)
	"""

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

		fn = abd + os.sep + 'html' + os.sep + "simpleresponse.html"
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
			<div>
			""" %(k,str(self.environ[k]))
			hwc.addcell(h2oo(s,'s'))


		#return these to gate.py
		return (status,response_headers,page.html())
