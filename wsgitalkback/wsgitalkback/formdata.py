"""
formdata.py
Author - Madhukumar Seshadri
Copyright (c) Madhukumar Seshadri
Purpose - Process posted forms
"""
from .transport import *
from urllib.parse import unquote_plus

class formdata:
	""" use fromrequest - works for all cases
		if you are in responder, simple self.processform works	
	"""
	@classmethod
	def fromrequest(cls,environ,encoding="utf-8"):
		""" 
			This can be called only once per request .. best way to get formdata
		    from post or from mulipart-boundary (browser provided forms)
			don't call this if you are getting the wsgi input and processing it
		"""
		req_m = environ["REQUEST_METHOD"]
		if req_m == "GET":
			return cls.fromurlenc(http_transport.xtract_qs(environ["QUERY_STRING"]))
		elif req_m == "POST":
			ptype,x = http_transport.xtract_posted(environ)
			#print ('formdata from request',ptype,x)
			if ptype == None:
				return None
			if ptype == 1:
				#multi-part form
				return cls.frommultipart(x)
			elif ptype == 0:
				#url encoded bytes - bytes can be encoded on client end to non-utf8
				#we support only what python supports - otherwise get the bytes from 
				#input() and decode yourself
				if not encoding:
					return cls.fromurlenc_bytes(http_transport.xtract_qs_from_bytes(x))
				else:
					return cls.fromurlenc(http_transport.xtract_qs(str(x,encoding)))
			elif ptype == 2:
				return cls.fromoctet(x)
		else:
			print("Only GET and POST are supported")
			return None

	@classmethod
	def frommultipart(cls,xstruct):
		""" where xstruct is ptree from xtract_multiplart in transport.py 
			formdata.data - {},
			formdat.data[fieldname] = [type,value,filename,content-type]
			type=b'f' if file otherwise b''
			value=bytes of file
			filename=b'' name of the file
			content-type=b'' content-type of the file
		"""
		instance=formdata()
		fieldname=''
		for key,value in xstruct:
			if key == b"transmission":
				instance.transmission=value
			elif key == b"boundary":
				instance.boundary=value;
			elif key == b"begin":
				start=1
			elif key == b'Content-Disposition' and start:
				output = http_transport.xtract_fv_bytes(value)
				for item in output:
					if item[0]==b"name":
						fieldname = item[1][1:-1]
						if fieldname in instance.data:
							if type(instance.data[fieldname][0]) == type([]):
								instance.data[fieldname].append([b'',b'',b'',b''])
							else:
								type_,value,filename,content_type=instance.data[fieldname]
								instance.data[fieldname]=[]
								instance.data[fieldname].append([type_,value,filename,content_type])
								instance.data[fieldname].append([b'',b'',b'',b''])
						else:
							instance.data[fieldname]=[b'',b'',b'',b'']
					elif item[0] == b"filename":
						if type(instance.data[fieldname][0]) == type([]):
							instance.data[fieldname][len(instance.data[fieldname])-1]=[b'f',b'',item[1],b'']
						else:
							instance.data[fieldname]=[b'f',b'',item[1],b'']
			elif key == b"Content-Type" and start:
				if type(instance.data[fieldname][0]) == type([]):
					instance.data[fieldname][len(instance.data[fieldname])-1][3]=value
				else:
					instance.data[fieldname][3]=value
			elif key == b'file' or key == b'field' and start:
				if type(instance.data[fieldname][0]) == type([]):
					instance.data[fieldname][len(instance.data[fieldname])-1][1]=value
				else:
					instance.data[fieldname][1]=value
			elif key == b'end':
				start = 0
				fieldname=''

		return instance

	@classmethod
	def fromurlenc_bytes(cls,qst):
		""" qst is output of http_transport.xtract_qs """
		instance=formdata()
		for apair in qst:
			#print("fromurlenc:",apair)
			name,value=apair
			#newme.fields.append(field(name,value))
			#type,value,filename,content-type
			instance.data[bytes(name)]=["",bytes(value),"",""]
		return instance

	@classmethod
	def fromurlenc(cls,qst,percent_decode=True):
		""" qst is output of http_transport.xtract_qs """
		instance=formdata()
		for apair in qst:
			name,value=apair
			#newme.fields.append(field(name,value))
			#type,value,filename,content-type
			if percent_decode:
				value = unquote_plus(value)
			instance.data[name]=["",value,"",""]
		return instance

	@classmethod
	def fromoctet(cls,octet):
		""" raw octet """
		instance=formdata()
		instance.data = octet
		return instance

	def __init__(self):
		self.data={}

	def __getitem__(self,k):
		return self.data[k]

	def keys(self):
		return list(self.data.keys())

	def __str__(self):
		return str(self.data)
