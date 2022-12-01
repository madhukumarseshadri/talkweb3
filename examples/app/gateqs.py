"""
Talkweb Examples
Author - Madhukumar Seshadri
gate.py
"""
from wsgitalkback import *
from wsgitalkback import fskeeper
#from talksql import *

def application(environ,start_response):
	""" default handler for http request """
	response = 'Cannot find requested page'
	response_headers=[]

	#get the uriresponder from responders
	uriresponder=responders.uriresponder()

	#why not implement a routing module - see readme.md
	#usession = Npne, cookies - None if not processed above
	#get to your responder - mapped via ?r=responderfile
	responder=uriresponder.respondfor(environ)

	#respond to the request
	status,xresponse_headers,response = responder.respond()

	for aheader in xresponse_headers:
		response_headers.append(aheader)

	#return the response
	start_response(status,response_headers)
	return [bytes(response,'utf-8')]