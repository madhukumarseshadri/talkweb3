"""
ajax responder
Author: Madhukumar Seshadri
Copyright (c) Madhukumar Seshadri
"""
from wsgitalkback import *
from talkweb import *

class myresponder(uiresponder):
	"""your response	"""

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

		self.processform()
		
		#return these to gate.py
		return (status,response_headers,"self.formdata.data:"+str(self.formdata.data))