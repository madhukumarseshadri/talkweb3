"""
myresponder
filename is used to call from url
Author: Madhukumar Seshadri
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

		hwc.addcell(h2oo("<div>URL Query string as formdata:"+\
						str(self.qs) +"</div>",'s'))

		hwc.addcell(h2oo("<div>URL Query string as formdata:"+\
						str(self.qsaofa) +"</div>",'s'))

		#add hello world cell from string by adding 's' to h2oo (html to object)
		qsformdata = formdata.fromurlenc(self.qsaofa)
		print('qsfomdata',qsformdata.data)

		hwc.addcell(h2oo("<div>URL Query string as formdata:"+\
						str(qsformdata.data) +"</div>",'s'))
		#return these to gate.py
		return (status,response_headers,page.html())
