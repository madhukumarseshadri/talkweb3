"""
Talkweb Examples
Author - Madhukumar Seshadri
"""
from talkback import *
#from talksql import *
import os

def application(environ,start_response):
	""" default handler for http request """
	appbasedir=os.path.dirname(__file__)
	#put the responder files under appbasedir/responders/

	#get the uriresponder from responders
	uriresponder=responders.uriresponder()

	router = appbasedir + os.sep + "routes"
	responder=uriresponder.responderfromroutes(appbasedir,environ,router)

	#respond to the request
	status,response_headers,response = responder.respond()

	start_response(status,response_headers)
	#don't hardcode utf-8, use the response_headers Content-Type and charset
	#or have respond provide the bytes
	return [bytes(response,'utf-8')]