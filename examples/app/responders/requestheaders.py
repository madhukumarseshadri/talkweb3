"""
request headers
filename is used to call from url
Author: Madhukumar Seshadri
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

		s = self.requestheader('rh1')

		#return these to gate.py
		return (status,response_headers,s)
