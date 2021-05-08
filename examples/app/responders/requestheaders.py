"""
request headers
filename is used to call from url
Author: Madhukumar Seshadri
Copyright (c) Madhukumar Seshadri
"""
from wsgitalkback import *
from talkweb import *

class myresponder(uiresponder):
	"""your response"""
	def respond(self):
		""" your response please """
		status = '200 OK'
		response_headers=[]

		s = self.requestheader('rh1')

		#return these to gate.py
		return (status,response_headers,s)
