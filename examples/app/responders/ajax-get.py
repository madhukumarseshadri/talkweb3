"""
ajax responder
Author: Madhukumar Seshadri
Copyright (c) Madhukumar Seshadri
"""
from talkback import *
from talkweb import *

class myresponder(uiresponder):
	"""your response	"""

	def respond(self):
		""" your response please """
		status = '200 OK'
		response_headers=[("Content-type","text/html;charset=utf-8;")]

		#print to apache log
		#print('an',an,'wan',wan,'abd',abd)

		self.processform()
		
		#return these to gate.py
		return (status,response_headers,"formdata:"+str(self.formdata.data))