""" 
headers.py
Author - Madhukumar Seshadri
RFC 2616 - HyperText Transfer Protocol (RFC2616 4.2 http://www.ietf.org/rfc/rfc2616.txt)
RFC 2965 - defines Cookie protocols over http response header protocols on RFC 2616 4.2
   cookie:*name=value; comment version=;path=;comment=;
	expires=;max_age,)(domain,),(commentURL,),(port,),discard;secure;httponly;
Set-Cookie:name=value,
Features that not there but you can get from Cookie.py in mod_python:
	pyobject serialize to wire as field content
	encrypted cookies

xtract
	query string 
	cookies
	posted
		form-data - "application/x-www-form-urlencoded"
		multipart-formdata - with files

We estimate this took close to 10-12 days and that is really annoying author is not good
"""
import time
import re
import sys

class cparser:
	whitespace=' '
	esc ="\\"
	newline="\n"
	tab="\t"
	wb=[whitespace,tab,newline]
	eol='eol'
	
	@classmethod
	def search(cls,charset,s,start=0):
		""" search for set of char in given charset (list) within s starting from start """
		for i,c in enumerate(s):
			if c in charset and i >= start:
				return (i,c)
		return (-1,0)
	
	@classmethod
	def isabreaker(cls,c,alist,esc):
		""" where we find char in c within a list alist that is not escaped by esc """
		### if c is char and esc is escape character and alist is a list, we find whether c is in alist unescaped
		for i,x in enumerate(alist):
			if c==x and alist[i-1] != esc:
				return x
		return 0
	
	@classmethod
	def parse(cls,text,start,l,breakers=wb,esc=esc):
		""" parse the text for breakers from start to l and
			return till breaker, broken char or cls.eol and index of break
			"""
		brokeon=None
		prc=c=""; sequence=""
		i=start+1
		#print ("cparser:cparse>","input:",text,"start:",start,"length:",l,"breakers:",breakers)
		while i < l:
			c = text[i]
			if c in breakers and prc != esc:
				output=(sequence,c,i)
				brokeon=c
				break
			elif c in breakers and prc == esc:
				sequence=sequence[0:-1]
				sequence += c
				prc=c
				i += 1
				continue
			else:
				sequence += c
				prc=c
				i += 1
		if not brokeon:
			output=(sequence,cls.eol,i)
		#print ("cparser:cparse>output",output)
		return output
	
	@classmethod
	def lines(cls,ofstr):
		""" where lines in a string separated by newline comes to (list-of-lines,total-lines) """
		output=[]
		i=-1;l=len(ofstr)
		line,b,i=cls.parse(ofstr,i,len(ofstr),cls.newline)
		while (b is not cls.eol):
			output.append(line)
			line,b,i=cls.parse(ofstr,i,len(ofstr),cls.newline)
		output.append(line)
		return output
	
	
	@classmethod
	def decomment(cls,line,char="/",repeat=2,esc="\\"):
		""" where we decomment comments char is a single
			that need to be repeated atleast 2 times or repeat times
			line that need to be decommented
			Note - There is escape of comment with esc
			"""
		prevprevc=prevc=o="";
		dqon=sqon=mpos=commenton=0
		ccount=1
		firstentry=1
		for i,c in enumerate(line):
			if commenton:
				if firstentry:
					o = o[0:len(o)-repeat]
					firstentry=0
				continue
			elif c == '"':
				if dqon:
					dqon=0
				else:
					dqon=1
				o +=c
			elif c == "'":
				if sqon:
					sqon=0
				else:
					sqon=1
				o +=c
			elif c==char and not sqon and not dqon:
				if prevc == c:
					ccount += 1
				else:
					ccount = 1
				
				o+=c
				
				if ccount == repeat:
					if prevprevc == esc:
						commenton = 0
						cc=""
						for i in range(repeat):
							o=o[0:-1]
							cc += char
						o=o[0:-1] + cc
					else:
						commenton = 1
			else:
				o += c
			
			if prevc:
				prevprevc=prevc
			prevc=c
		return o
	
	@classmethod
	def rstr(x):
		""" reverse a string """
		output=""
		r=range(len(x))
		r.reverse()
		for i in r:
			output += x[i]
		return output
	
	@classmethod
	def display(cls,s):
		out=""
		for c in s:
			if c == cls.whitespace:
				out += "<s>"
			elif c == cls.tab:
				out += "<tab>"
			elif c == cls.newline:
				out += "<cr>"
			else:
				out += c
		return out


def find(s,start,seq,l):
	""" extract till a sequence occurs """	
	#slen=len(s)
	wlen = len(seq)
	cc=s[start:start+wlen]
	while (cc != seq and start < l):
		#print (cc)
		start += 1
		cc = s[start:wlen+start]
	return start

def findany(s,start,seq,l):
	while start < l:
		if s[start] in seq:
			return start
		start += 1
	return l

class html_transport:
	""" vocab for rfc2616 http://www.ietf.org/rfc/rfc2616.txt """
	sq="'"; dq='"';eq="="
	comment=";"
	lf="\n"; cr="\r"; sp=" "; ht="\t";crlf=cr+lf
	amp="&"; colon=":"; semicolon=";"; comma=","
	esc="\\"
	#esc is break in rfc
	#qssep=amp+eq+semicolon
	qssep=[amp,eq,semicolon]
	cookiesep="()<>[]{}@/?"+eq+sq+dq+sp+ht+lf+cr+colon+comma+semicolon
    
	@classmethod
	def xtract_cookies(cls,s):
		""" 	where we extract the cookie from http heder field to a dict of key/val pairs
			from s is rfc2616 complaint header field content that is complaint to rfc2965 complaint fvps
				grammar of message-header in rfc2616:
				field-name=token (anything that breaks on defined separator)
				filed-content = <the OCTETs making up the field-value and 
					consisting of either *TEXT or combinations of token, separators and quoted-string>
 				field-value = 0*n(field-content | LWS)
				message-header = field-name":"[field-value]
		"""
		output=[]
		ww=prk=""; eqon=opendq=0
		i=-1;l=len(s)
		if l == i:	return output
		w,b,i=cparser.parse(s,i,l,cls.cookiesep,cparser.esc)
		while (b is not cparser.eol):
			if b is cls.dq and opendq:
				opendq=0
				ww += w + '"'
			elif b is cls.dq and not opendq:
				opendq=1
				ww += w + '"'
			elif b is cls.eq and not opendq:
				output.append([w,""])
				ww=""
				eqon=1
			elif b in [cls.semicolon] and not opendq:
				if eqon:
					eqon=0
					ww += w
					le=len(output)-1
					if le > -1:
						output[le][1]=ww
				else:
					output.append([w,""])
			#@todo (post checking spec) elif b in [cls.cr,cls.lf,cls.crlf]:
			else:
				ww += w + b
		
			w,b,i=cparser.parse(s,i,l,cls.cookiesep,cls.esc)

		if w or ww:
			ww += w
			le=len(output)-1
			if le > -1:
				output[le][1]=ww

		"""
		for key,value in output:
			if value:
				print (key +"="+ value +";")
			else:
				print (key + ";" )"""

		return output

	@classmethod
	def xtract_qs(cls,incoming,encoding="utf-8"):
		""" 	where we extract url encoded qs - it seems qs is part of cgi spec as 
			rfc 1808, rfc 1738
			use to xtract anything that is urlenc
		"""
		output=[]
		if not incoming:
			return output
		if type(incoming) != type(''):
			s = incoming.decode(encoding)
		else:
			s = incoming
		lhs="";i=-1;l=len(s);
		w,b,i=cparser.parse(s,i,l,cls.qssep,cparser.esc)
		while (b is not cparser.eol):
			if b is cls.eq:
				lhs=w
			elif b is cls.amp or cls.semicolon:
				#output.append([lhs,w])
				output.append([lhs,w.replace("+"," ")])
				lhs=""
			w,b,i=cparser.parse(s,i,l,cls.qssep,cls.esc)
		if lhs:
			#output.append([lhs,w])
			output.append([lhs,w.replace("+"," ")])

		return output

	@classmethod
	def xtract_multipart(cls,octet,boundary):
			""" @todo rewrite """
			ptree=[]
			ptree.append(["boundary",boundary])
			ptree.append(["transmission",octet])

			l = len(octet)
			lhs=""
			wb=[cls.cr,cls.lf,cls.colon]
			# semi and sq
			i=-1;pi=len(ptree)-1;
			w,b,i = cparser.parse(octet,i,l,wb)

			#@todo cparser parses non esc based parsing
			while (b is not cparser.eol):
				if re.match(".+"+boundary,w):
					ptree.append([w,"boundary"]); pi += 1
					if lhs == "contents":
						lhs = ""
				elif b is cls.colon and w:
					lhs=w
					ptree.append([w,""])
					pi += 1
					if lhs.lower() == "content-type":
						#@todo this is an assumption that content will follow the content-type
						till = i
						till=findany(octet,i+1,cls.cr+cls.lf,l)
						ptree[pi][1]=octet[i+1:till]; i = till + 1
						till=find(octet,i+1,boundary,l)
						ptree.append(["file",octet[i:till-2]]); pi += 1;
						i = till + len(boundary) + 1
						lhs="file"
				elif b in [cls.cr,cls.lf] and w:
					if lhs:
						#ptree[pi][1] = w
						ptree[pi][1] = cls.xtract_cookies(w)
					else:
						ptree.append(["",w]); pi += 1
					lhs=""

				w,b,i = cparser.parse(octet,i,l,wb)

			return ptree


	@classmethod 
	def xtract_posted(cls,environ):
		""" 	where req is request object
			@todo request object makes this lib dependent to mod_python
			challenge is extra read that we do get the posted based on the content length
			in typed system, code will require some thoughts before migrating
			if url encoded which is default for form, 
			A) output can be (None,"") if there is no content-type in the header
			B) if content-type is form post - output will be (0,throw this member of list to formdata.frompost_urlencoded)
			C) output will be (1,throw this member of this list to formdata.frompost_multipart)
		"""
		#print "xtract_posted"
		l=0;octet="";proceed=0
		boundary=""
		boundaries=[]
		#print (environ)
		incoming_type="CONTENT_TYPE"
		incoming_length="CONTENT_LENGTH"
				
		if incoming_type not in environ:
			return (None,incoming_type + " not in environ")

		if incoming_length in environ:
			l=int(environ[incoming_length])
		
		if l < 1:
			return (None,incoming_length + " is zero or less than zero")
		
		
		incoming = environ["wsgi.input"]
		incomingtype = environ[incoming_type]
		typeparts=incomingtype.split(";")
		stype=typeparts[0].strip()

		if  incomingtype == "application/x-www-form-urlencoded":
			proceed=1;
		elif stype == "multipart/form-data":
			b=typeparts[1].strip()
			boundary=b.split("=")
			boundary=boundary[1]
			proceed=2
		else:
			proceed=3

		octet = incoming.read(l)
		output=[]
		if proceed == 2:
			output=(1,cls.xtract_multipart(octet,boundary))
		elif proceed == 1:
			output=(0,octet)
		else:
			output=(2,octet)

		return output
