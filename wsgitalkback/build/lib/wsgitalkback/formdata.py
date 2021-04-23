""" 
formdata.py
Author - Madhukumar Seshadri
"""
from .headers import *
from urllib import *
from urllib.parse import *

class formdata:
	""" once processed from request cls.from request
		you get an instance of me ..  
		>> instance.formdata.data={fieldname:[type,value,filename,content-type], .. } 	"""
	@classmethod
	def fromrequest(cls,environ):
		""" this can be called only once per request .. best way to get formdata
		    from post or from mulipart-boundary (browser provided forms) 
		"""
		ptype,x = html_transport.xtract_posted(environ)
		#print ('formdata from request',ptype,x)
		if ptype == None:
			return None
		if ptype == 1:
			return cls.frommultipart(x)
		elif ptype == 0:
			return cls.fromurlenc(html_transport.xtract_qs(x))
		elif ptype == 2:
			return cls.fromoctet(x)

	@classmethod
	def frommultipart(cls,xstruct):
		""" where xstruct is struct xtract from headers.py """
		instance=formdata()
		contentdisposition=boundary=readyforfile=0;
		for key,value in xstruct:
			key = key.lower()
			if key == "transmission":
				instance.transmission=value
			elif key == "boundary":
				boundary=1;
			elif value == "boundary":
				boundary=0; 
				if contentdisposition:
					contentdisposition=0;
				continue
			elif contentdisposition and not key:
					#in xstruct - afield's value that is not file .. 
					#dealing with ['', 'Pick your user id'] 
					#instance.data[lastkey]["value"]=value
					instance.data[lastkey][1]=value
					lastkey=None
			elif key == "content-disposition":
				contentdisposition=1
				#going to in to decipher .. ['Content-Disposition', [['form-data', ''], ['name', '"userid"']]]
				fd=0
				for k,v in value:
					k = k.lower()
					if k == "form-data":
						fd=1
					elif k == "name" and fd:
						lastkey=v[1:-1]
						#instance.data[lastkey]={"value":"","type":None}
						instance.data[lastkey]=["","","",""]	#type,value,filename,content-type
					elif k == "filename" and fd:
						#instance.data[lastkey][k]=v[1:-1].strip()
						#instance.data[lastkey]["type"]="file"
						instance.data[lastkey][0]="f"
						instance.data[lastkey][2]=v[1:-1].strip()
			elif contentdisposition and key == "content-type":
					#instance.data[lastkey]["content-type"]=value.strip()
					instance.data[lastkey][3]=value.strip()
					readyforfile=1
			elif readyforfile and key == "file":
					#instance.data[lastkey]["value"]=value;
					instance.data[lastkey][1]=value[1:-1].strip();
					readyforfile=0
					lastkey=None

		#debug: logthis(req,"returning from from multipart ..")
		#debug: logthis(req,str(instance.data))
		return instance

	@classmethod
	def fromurlenc(cls,qst):
		""" qst is output of cls.xtract_qs """
		instance=formdata()
		for apair in qst:
			#logthis(req,"fromurlenc:",apair)
			name,value=apair
			#newme.fields.append(field(name,value))
			#type,value,filename,content-type
			instance.data[name]=["",unquote(value),"",""]
		return instance

	@classmethod
	def fromoctet(cls,octet):
		""" raw octet """
		instance=formdata()
		instance.data = octet
		return instance

	def __init__(self):
		self.data={}


"""
as sample of xstruct 
at Wed Aug 28 06:07:23 2013:xstruct
at Wed Aug 28 06:07:23 2013:['boundary', '---------------------------88178448610633266011591823221']
at Wed Aug 28 06:07:23 2013:['transmission', '-----------------------------88178448610633266011591823221\r\nContent-Disposition: form-data; name="username"\r\n\r\nFirst name Last name\r\n-----------------------------88178448610633266011591823221\r\nContent-Disposition: form-data; name="userid"\r\n\r\nPick your user id\r\n-----------------------------88178448610633266011591823221\r\nContent-Disposition: form-data; name="password"\r\n\r\n\r\n-----------------------------88178448610633266011591823221\r\nContent-Disposition: form-data; name="photo"; filename="Problems "\r\nContent-Type: application/octet-stream\r\n\r\nTalk Problems \n\n\n1) There was a discussion of getting the translator as it stand its today into a tree \n\tand it has been done as well somewhere \n2) \n\n1) twasks processing is crap - there are more asks from talkweb .. but there are hooks .. \n2) added ask of no trumpheting but it is still trumpheting\n3) xattrib - not sure where the switch is to turn off the style auto generation\n4) inline the page level scripts always unless overridden and keep the opening page to https\n\n\n\njava | activex | flash | html 5 | browser specific situation\n\t\n\r\n-----------------------------88178448610633266011591823221--\r\n']
at Wed Aug 28 06:07:23 2013:['-----------------------------88178448610633266011591823221', 'boundary']
at Wed Aug 28 06:07:23 2013:['Content-Disposition', [['form-data', ''], ['name', '"username"']]]
at Wed Aug 28 06:07:23 2013:['', 'First name Last name']
at Wed Aug 28 06:07:23 2013:['-----------------------------88178448610633266011591823221', 'boundary']
at Wed Aug 28 06:07:23 2013:['Content-Disposition', [['form-data', ''], ['name', '"userid"']]]
at Wed Aug 28 06:07:23 2013:['', 'Pick your user id']
at Wed Aug 28 06:07:23 2013:['-----------------------------88178448610633266011591823221', 'boundary']
at Wed Aug 28 06:07:23 2013:['Content-Disposition', [['form-data', ''], ['name', '"password"']]]
at Wed Aug 28 06:07:23 2013:['-----------------------------88178448610633266011591823221', 'boundary']
at Wed Aug 28 06:07:23 2013:['Content-Disposition', [['form-data', ''], ['name', '"photo"'], ['filename', '"Problems "']]]
at Wed Aug 28 06:07:23 2013:['Content-Type', ' application/octet-stream']
at Wed Aug 28 06:07:23 2013:['file', '\n\r\nTalk Problems \n\n\n1) There was a discussion of getting the translator as it stand its today into a tree \n\tand it has been done as well somewhere \n2) \n\n1) twasks processing is crap - there are more asks from talkweb .. but there are hooks .. \n2) added ask of no trumpheting but it is still trumpheting\n3) xattrib - not sure where the switch is to turn off the style auto generation\n4) inline the page level scripts always unless overridden and keep the opening page to https\n\n\n\njava | activex | flash | html 5 | browser specific situation\n\t\n\r\n'] 
"""
