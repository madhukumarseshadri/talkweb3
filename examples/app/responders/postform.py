"""
myresponder
filename is used to call from url
all responders are myresponders if you did not notice
Copyright (c) Madhukumar Seshadri
"""
from talkback import *
from talkweb import *

class myresponder(uiresponder):
	"""your response"""
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

		self.processform()

		#self.formdata.data is bytes not python strings if posted
		hwc.addcell(h2oo("<div>Post Form Values:"+\
						 str(self.formdata.data) +"</div>",'s'))

		#return these to gate.py
		return (status,response_headers,page.html())