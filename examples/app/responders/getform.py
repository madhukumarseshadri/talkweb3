"""
getform responder
all responders are myresponders if you did not notice
Copyright (c) Madhukumar Seshadri
"""
from talkback import *
from talkweb import *

class myresponder(uiresponder):
	""" your response	"""
	def respond(self):
		""" your response please """
		status = '200 OK'
		response_headers=[("Content-type","text/html;charset=utf-8;")]
		
		fn = self.appbasedir + os.sep + 'html' + os.sep + "simpleresponse.html"
		#come to object (cells) from html file
		page=h2oo(fn)
		#find the hello world container cell within the page
		hwc=page.findcellbyid("response")

		self.processform()

		#datatype,value,filename if file is being send, content_type of file
		type,value,filename,content_type=self.formdata.data['field1']

		#add hello world cell from string by adding 's' to h2oo (html to object)
		hwc.addcell(h2oo("<div>Get Form Values formdata in responder:"+\
					str(self.formdata.data) +"</div>",'s'))

		#return these to gate.py
		return (status,response_headers,page.html())
