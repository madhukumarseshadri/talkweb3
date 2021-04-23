"""
Talkweb Examples
gate.py
A facade to load responders for each http request
This example uses wsgitalkback to manage session and cookie
"""
from wsgitalkback import *

def application(environ,start_response):
	""" default handler for http request """
	status = '200 OK'
	output = 'Cannot find requested page '

	abd = appbasedir(environ)
	import sys
	sys.path.append(abd + os.sep + "responders")
	import config

	usession=None
	sk = sqlsessionkeeper(config.ipcfg)

	cookies=html_cookies.fromrequest(environ)
	sessioncookie=None
	for acookie in cookies:
		if acookie.name == "TALKWEB_EXAMPLE":
			sessioncookie = acookie
	
	if sessioncookie:
		usession = sk.get(sessioncookie.value)

	response_headers=[]
	if not usession:
		usession = session()
		scookie = cookie("TALKWEB_EXAMPLE",usession.id)
		scookie.sethttponly()
		scookie.setsamesite("lax")
		sk.put(usession)

		#scookie.setsecure()
		response_headers=html_cookies.toinject([scookie])

	responder=responders.uriresponder()
	pageresponder=responder.respondfor(environ,usession,cookies)

	if pageresponder:
		status,xresponse_headers,output=pageresponder.respond()
		if not status:
			status = '200 OK'
		if "Content-type" not in xresponse_headers:
			response_headers.append(("Content-type","text/html;charset=utf-8;"))
		if "Content-Length" not in xresponse_headers:
			response_headers.append(("Content-Length",str(len(output))))

		for aheader in xresponse_headers:
			response_headers.append(aheader)

	start_response(status,response_headers)
	return [bytes(output,'utf-8')]
