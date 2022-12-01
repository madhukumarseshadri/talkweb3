"""
cookie.py
Author - Madhukumar Seshadri
Copyright (c) Madhukumar Seshadri
HyperText Transfer Protocol (RFC2616 4.2 http://www.ietf.org/rfc/rfc2616.txt)
RFC 822
RFC 2965 - defines Cookie protocols over http response header protocols on RFC 2616 4.2
   cookie:*name=value; comment version=;path=;comment=;
	expires=;max_age,)(domain,),(commentURL,),(port,),discard;secure;httponly;
Set-Cookie:name=value,
Features that not there but you can get from Cookie.py in mod_python:
	pyobject serialize to wire as field content
	encrypted cookies
Purpose - Manage cookies as per RFC
"""
from .transport import *

class cookie:
	""" payload object """
	timeformat="%a, %d-%b-%Y %H:%M:%S GMT"
	#timeformat="%a %d %b %Y %H:%M:%S GMT"
	def __init__(self,withname,value):
		""" withname - call you cookie and set a valid python object
			only strings are possible in this version  """
		self.name=withname
		self.value=value
		self.nvp={}
	def __str__(self):
		return self.asfv()
	def _setnvp(self,key,value):
		self.nvp[html_cookies.enumforkey(key)]=value
	def setversion(self,version):
		self.nvp[html_cookies.enumforkey("version")]=version
	def setpath(self,path):
		self.nvp[html_cookies.enumforkey("path")]=path
	def setdomain(self,domain):
		self.nvp[html_cookies.enumforkey("domain")]=domain
	def setcomment(self,comment):
		self.nvp[html_cookies.enumforkey("comment")]=comment
	def setexpiry(self,dt):
		""" expects a datetime object as input"""
		self.nvp[html_cookies.enumforkey("expires")]= dt.strftime(cookie.timeformat)
	def expires(self,ina,unit):
		""" ina is number and unit is s/h/d/w/m/y for seconds,hours,days,weeks,month and years respectively """
		return None
	def setmaxage(self,age):
		self.nvp[html_cookies.enumforkey("max_age")]=age
	def setcommentURL(self,url):
		self.nvp[html_cookies.enumforkey("commentURL")]=url
	def setport(self,port):
		self.nvp[html_cookies.enumforkey("port")]=port
	def setdiscard(self):
		self.nvp[html_cookies.enumforkey("discard")]=""
	def setsecure(self):
		self.nvp[html_cookies.enumforkey("secure")]=""
	def sethttponly(self):
		self.nvp[html_cookies.enumforkey("httponly")]=""
	def setsamesite(self,value):
		""" values are none, lax, strict"""
		self.nvp[html_cookies.enumforkey("samesite")]=value
	def asfv(self):
		""" as field content - where we bring the set attribs to rfc 2616 stream """
		s=""
		#@todo self.value need to be come to rfc complaint stream from pyobject
		s +=  self.name + http_transport.eq + str(self.value) + http_transport.semicolon
		for this_enum in self.nvp:
			if this_enum in html_cookies.novaluekeys:
				#secure, httponly, discard
				s += html_cookies.keyforenum(this_enum) + http_transport.semicolon
			else:
				s += html_cookies.keyforenum(this_enum) + \
					http_transport.eq + str(self.nvp[this_enum]) + http_transport.semicolon
		return s[0:-1]

class html_cookies:
	""" rfc 2965
		receive using html_cookies.fromrequest(request) returns a pylist of cookie objects
		send using html_cookies.inject(request,<modified pylistof cookies>)
	"""
	#name=value is outside of this
	keys=["version","path","domain","comment",\
		"expires","max_age","commentURL","port",\
		"discard","secure","httponly","samesite"]
	novaluekeys=[8,9,10]
	request_header_key="cookie"
	response_header_key="Set-Cookie"

	@classmethod
	def keyforenum(cls,enum):
		""" name of key for enum"""
		if enum < len(cls.keys):
			return cls.keys[enum]

	@classmethod
	def enumforkey(cls,key):
		""" index for key """
		for i,akey in enumerate(cls.keys):
			if akey == key:
				return i

	@classmethod
	def generate(cls,s):
		""" we bring cookies object to life
		    s is whatever in http_transport xtracted_cookies output
		    if you provide output which need to be cookies you get cookies in your cookies
		    or we create and give it you """
		output=[]
		newcookie=None
		for key,value in s:
			if key not in cls.keys:
				if newcookie is None:
					newcookie=cookie(key,value)	#first cookie
					continue
				else:
					output.append(newcookie)
					newcookie=cookie(key,value)
			else:
				if newcookie:
					newcookie._setnvp(key,value)
		if newcookie:
			output.append(newcookie)

		#print ("cls.generate",output)
		return output

	@classmethod
	def fromrequest(cls, environ):
		""" generate from request """
		if not environ:
			return
		if "HTTP_COOKIE" not in environ:
			return []
		s=environ["HTTP_COOKIE"]
		xtracted=http_transport.xtract_cookies(s)
		#print("xtracted cookies", xtracted)
		return cls.generate(xtracted)

	@classmethod
	def toinject(cls,alist):
		response_headers=[]
		for acookie in alist:
			response_headers.append((html_cookies.response_header_key,acookie.asfv()))

		return response_headers


if __name__ == "__main__":
	print ("testing cookie.py .. if you see this you need to comment this out before deployment")
	print ("making cookies in server memory .. ")
	#mycookies=[cookie("pecan",[1,2,3,4]),cookie("choclate-chip",{1:2,3:4})]
	#mycookies[0].setversion("1.0")
	#mycookies[0].setpath("\"god knows\"")
	#mycookies[0].setdomain("/something/something/something ..")
	#mycookies[0].setcomment("what the ")
	#mycookies[0].setexpiry(time.gmtime())
	#mycookies[0].setmaxage(2)
	#mycookies[0].setcommentURL("/na/baby/babyna")
	#mycookies[0].setport(390)
	#mycookies[0].setdiscard()
	#mycookies[0].setsecure()
	#mycookies[0].sethttponly()
	#mycookies[0].setdiscard()
	#mycookies[0].setsecure()
	#mycookies[0].sethttponly()
	#s=cookies(mycookies).inject()
	#print "injected string in http header .."
	#print s
	s='choclatechip="what good are you"; pecan=[1, 2, 3, 4]'
	print ("coming to object")
	print ("received:",s)
	xtracted=http_transport.xtract_cookies(s)
	print ("xtracted:",xtracted)
	mycookies=html_cookies.generate(xtracted)
	print (html_cookies.toinject(mycookies))
