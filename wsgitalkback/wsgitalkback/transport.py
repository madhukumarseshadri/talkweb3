"""
transport.py
Author - Madhukumar Seshadri
Copyright (c) Madhukumar Seshadri
RFC 2616 - HyperText Transfer Protocol (RFC2616 4.2 http://www.ietf.org/rfc/rfc2616.txt)
RFC 1867 - Form based file upload https://tools.ietf.org/html/rfc1867
RFC 2854 - obseltes 1867 https://tools.ietf.org/html/rfc2854
RFC 2965 - defines Cookie protocols over http response header protocols on RFC 2616 4.2
   cookie:*name=value; comment version=;path=;comment=;
	expires=;max_age,)(domain,),(commentURL,),(port,),discard;secure;httponly;
Set-Cookie:name=value,
https://url.spec.whatwg.org/#application/x-www-form-urlencoded

Purpose - xtract
	query string from url
	query string bytes from posted form-data
	cookies
	posted
		form-data - "application/x-www-form-urlencoded"
		multipart-formdata - with files
"""
import re
from .parse import *

class http_transport:
	""" rfc2616 http://www.ietf.org/rfc/rfc2616.txt """
	sq="'"; dq='"';eq="="
	comment=";"
	lf="\n"; cr="\r"; sp=" "; ht="\t";crlf=cr+lf
	amp="&"; colon=":"; semicolon=";"; comma=","
	esc="\\"
	#esc is break in rfc
	#qssep=amp+eq+semicolon
	qssep=[amp,eq,semicolon];
	qs_bsep=b'&=;'
	cookiesep="()<>[]{}@/?"+eq+sq+dq+sp+ht+lf+cr+colon+comma+semicolon
	cookie_bsep=b'()<>[]{}@/?=\'" \t\n\r:,;'

	@classmethod
	def xtract_fv_bytes(cls,incoming):
		""" xtract field value pairs like cookies from bytes"""
		output=[]
		ww=bytearray();
		eqon=opendq=0
		i=-1;l=len(incoming)
		if l == i:	return output
		w,b,i=bparser.parse(incoming,i,l,cls.cookie_bsep)
		while (b is not cparser.eol):
			if b == b'"'[0] and opendq:
				opendq=0
				ww += w + b'"'
			elif b == b'"'[0] and not opendq:
				opendq=1
				ww += w + b'"'
			elif b == b'='[0] and not opendq:
				output.append([bytes(w),""])
				ww=bytearray()
				eqon=1
			elif b == b';'[0] and not opendq:
				if eqon:
					eqon=0
					ww += w
					le=len(output)-1
					if le > -1:
						output[le][1]=bytes(ww)
				else:
					output.append([w,""])
			#@todo (post checking spec) elif b in [cls.cr,cls.lf,cls.crlf]:
			else:
				ww += w
				ww.append(b)

			w,b,i=bparser.parse(incoming,i,l,cls.cookie_bsep)

		if w or ww:
			ww += w
			le=len(output)-1
			if le > -1:
				output[le][1]=bytes(ww)

		return output

	@classmethod
	def xtract_cookies(cls,s):
		""" 	where we extract the cookie from http header field to a dict of key/val pairs
			    from s is rfc2616 complaint header field content that is complaint to rfc2965 complaint fvps
				grammar of message-header in rfc2616:
				field-name=token (anything that breaks on defined separator)
				filed-content = <the OCTETs making up the field-value and
					consisting of either *TEXT or combinations of token, separators and quoted-string>
 				field-value = 0*n(field-content | LWS)
				message-header = field-name":"[field-value]
                in mod_wsgi this is in environ as a python string
		"""
		output=[]
		ww=prk=""; eqon=opendq=0
		i=-1;l=len(s)
		if l == i:	return output
		w,b,i=cparser.parse(s,i,l,cls.cookiesep)
		while (b is not cparser.eol):
			if b == cls.dq and opendq:
				opendq=0
				ww += w + '"'
			elif b == cls.dq and not opendq:
				opendq=1
				ww += w + '"'
			elif b is cls.eq and not opendq:
				output.append([w,""])
				ww=""
				eqon=1
			elif b == cls.semicolon and not opendq:
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

			w,b,i=cparser.parse(s,i,l,cls.cookiesep)

		if w or ww:
			ww += w
			le=len(output)-1
			if le > -1:
				output[le][1]=ww

		return output

	@classmethod
	def xtract_qs_from_bytes(cls,incoming):
		output=[]
		lhs="";i=-1;l=len(incoming);
		w,b,i=bparser.parse(incoming,i,l,cls.qs_bsep)
		while (b is not bparser.eol):
			if b == cls.qs_bsep[1]:
				lhs=w
			elif b == cls.qs_bsep[0] or b == cls.qs_bsep[2]:
				#output.append([lhs,w])
				output.append([lhs,w.replace(b'+',b' ')])
				lhs=""
			w,b,i=bparser.parse(incoming,i,l,cls.qs_bsep)
		if lhs:
			#output.append([lhs,w])
			output.append([lhs,w])

		return output

	@classmethod
	def xtract_qs(cls,incoming):
		""" incoming is string not bytes
			where we extract url encoded qs - it seems qs is part of cgi spec as
			rfc 1808, rfc 1738
			use to xtract anything that is urlenc
		"""
		output=[]
		lhs="";i=-1;l=len(incoming);
		w,b,i=cparser.parse(incoming,i,l,cls.qssep)
		while (b is not cparser.eol):
			if b == cls.eq:
				lhs=w
			elif b == cls.amp or b == cls.semicolon:
				#output.append([lhs,w])
				output.append([lhs,w.replace("+"," ")])
				lhs=""
			w,b,i=cparser.parse(incoming,i,l,cls.qssep)
		if lhs:
			#output.append([lhs,w])
			output.append([lhs,w])

		return output

	@classmethod 
	def xtract_one(cls,rest,ptree):
		content_type=content_disposition=b''
		#content disposition
		m = re.search(b'Content-Disposition:',rest)
		start,stop = m.span()
		rest = rest[stop:]
		m = re.search(b'\r\n',rest)
		start,stop = m.span()
		content_disposition = rest[:stop-2]
		rest = rest[stop:]
		#content type
		content_type=b''
		m = re.search(b'Content-Type:',rest)
		if m:
			start,stop = m.span()
			rest = rest[stop:]
			m = re.search(b'\r\n',rest)
			start,stop = m.span()
			content_type = rest[:stop-2]
			rest = rest[stop:]
		#transfer encoding
		content_transfer_encoding=b''
		m = re.search(b'Content-Transfer-Encoding:',rest)
		if m:
			start,stop = m.span()
			rest = rest[stop:]
			m = re.search(b'\r\n',rest)
			start,stop = m.span()
			content_transfer_encoding = rest[:stop-2]
			rest = rest[stop:]
		#begin content block
		m = re.search(b'\r\n',rest)
		start,stop = m.span()
		rest = rest[stop:]
		content = rest[:start-4]
		#print("block processing done",rest)
		ptree.append([b'begin',''])
		ptree.append([b'Content-Disposition',content_disposition])
		if content_type:
			ptree.append([b'Content-Type',content_type])
			content_type=b'file'
		else:
			content_type=b'field'
		if content_transfer_encoding:
			ptree.append([b'Content-Transfer-Encoding',content_transfer_encoding])
		ptree.append([content_type,content])
		ptree.append([b'end',''])

	@classmethod
	def xtract_multipart(cls,octet,boundary):
		""" xtract multipart form data """ 
		ptree=[]
		#ptree.append([b"boundary",boundary])
		#ptree.append([b"transmission",octet])
		l = len(octet)
		m = re.search(boundary,octet)
		start,stop = m.span()
		rest = octet[stop:]
		while rest:
			m = re.search(boundary,rest)
			start,stop = m.span()
			one = rest[:start]
			rest = rest[stop:]
			cls.xtract_one(one,ptree)
			if rest[:-2] == b'--':
				break

		return ptree

	@classmethod
	def xtract_posted(cls,environ):
		"""
			Need to get rid of proceed if content-length is immaterial
			if url encoded which is default for form,
			A) output can be (None,"") if there is no content-type in the header
			B) if content-type is form post - output will be (0,throw this member of list to formdata.frompost_urlencoded)
			C) output will be (1,throw this member of this list to formdata.frompost_multipart)
		"""
		l=0;octet=b"";proceed=0
		boundary=b""

		#if "CONTENT_TYPE" not in environ:
		#	return (None, "CONTENT_TYPE not in environ")

		#if "CONTENT_LENGTH" in environ:
		#	l=int(environ["CONTENT_LENGTH"])

		#if l < 1:
		#	return (None,incoming_length + " is zero or less than zero")

		incoming = environ["wsgi.input"]
		incomingtype=""
		if "CONTENT_TYPE" in environ:
			incomingtype = environ["CONTENT_TYPE"]

		typeparts=incomingtype.split(";")
		firstpart=typeparts[0].strip()

		if  incomingtype == "application/x-www-form-urlencoded":
			proceed=1;
		elif firstpart == "multipart/form-data":
			b=typeparts[1].strip()
			boundary=b.split("=")
			boundary=bytes(boundary[1],"utf-8")
			proceed=2
		else:
			proceed=3

		#proceed was done for reading till content length
		#now reading everything as mod_wsgi specs state you 
		#can read until wsgi.input returns ''
		inp = incoming.read(1024*1024)
		while inp:
			octet += inp
			inp = incoming.read(1024*1024)

		output=[]
		if proceed == 2:
			output=(1,cls.xtract_multipart(octet,boundary))
		elif proceed == 1:
			output=(0,octet)
		else:
			output=(2,octet)

		return output

if __name__ == "__main__":
    #qs = b'?r=madhu&s=m&x=%7B%'
    #xtracted = http_transport.xtract_qs_from_bytes(qs)
    #print(xtracted)
	transmission=open("/tmp/octet.t","rb").read()
	boundary = b'------WebKitFormBoundarye6ggrdOhhDvOxLrM'
	for item in http_transport.xtract_multipart(transmission,boundary):
		print(item)