""" 
app.py
Author - Madhukumar Seshadri
Copyright (c) Madhukumar Seshadri
Purpose - provide app related items to app from environ
"""
import os
import sys
import time
from .path import *

def appname(environ):
	p = pathpieces(environ["SCRIPT_FILENAME"])
	return p[0][len(p[0])-2]

def appbasedir(environ):
	return pathfile(environ["SCRIPT_FILENAME"])[0]
	
def htdocsbasedir(environ):
	"""		@todo - unncessary two calls
	"""
	return environ['DOCUMENT_ROOT']

def wsgialias(environ):
	return environ ['SCRIPT_NAME']
	
def sysuser():
	f=os.popen("ps -ef | egrep -i $(echo $$) | awk '{ if (NR==1) print $1; }'")
	return f.read()

def logtoos():
	pass

def logtowebserver():
	pass

def logthis(*args):
	""" environ is first arg followed as many as python stack would allow """
	print (args[1:])

if __name__ == "__main__":
	environ={}
	environ["SCRIPT_FILENAME"]=""
	print (appbasedir(environ))
	print (appname(environ))
	print (htdocsbasedir())
