"""
myresponder
filename is used to call from url
Author: Madhukumar Seshadri
Copyright (c) Madhukumar Seshadri
"""
from talkback import *
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
		response_headers=[("Content-type","text/html;charset=utf-8;")]
		
		#print to apache log
		#print('an',an,'wan',wan,'abd',abd)
		print(self.scriptname())

		fn = self.appbasedir + os.sep + 'html' + os.sep + "simpleresponse.html"
		#come to object (cells) from html file
		page=h2oo(fn)
		#find the hello world container cell within the page
		hwc=page.findcellbyid("response")

		hwc.addcell(h2oo("<div>URL Query string:"+\
						str(self.qs) +"</div>",'s'))

		qsaofa=http_transport.xtract_qs(self.qs)
		hwc.addcell(h2oo("<div>URL Query string as Array of Array:"+\
						str(qsaofa) +"</div>",'s'))

		#add hello world cell from string by adding 's' to h2oo (html to object)
		qsformdata = formdata.fromurlenc(qsaofa)

		hwc.addcell(h2oo("<div>URL Query string as formdata:"+\
						str(qsformdata.data) +"</div>",'s'))
		#return these to gate.py
		return (status,response_headers,page.html())
