"""
main
filename is used to call from url
all responders are myresponders if you did not notice
Copyright (c) Madhukumar Seshadri
"""
from talkback import *
from talkweb import *

class myresponder(uiresponder):
	"""  self.environ self.usession and self.cookies """
	def respond(self):
		""" your response please """
		status="200 OK"
		response_headers=[("Content-type","text/html;charset=utf-8;")]
				
		self.processform(encoding=None)
		
		#type,value,filename,content_type = self.formdata.data[b'fieldname']
		#note - fieldname is bytes in mutlipart/formdata
		#if input is multiple, self.formdata.data[b'fieldname'] will be an array of 
		#type,value,filename,content_type
		#you need to know whether input or multiple or single if not
		#you check for type of self.formdata[b['fieldname']]
		_,id,_,_=self.formdata[b'id']
		
		s=""
		if type(self.formdata[b"file1"][0]) == type([]):
			for type_,value,filename,content_type in self.formdata[b'file1']:
				filename = filename.decode("utf-8")[1:-1]
				f = open("/tmp/"+filename,"wb")
				f.write(value)
				s += '/tmp/'+filename + " "
			s = s[:-1]
		else:
			type_,value,filename,content_type = self.formdata[b'file1']
			filename = filename.decode("utf-8")[1:-1]
			f = open("/tmp/"+filename,"wb")
			f.write(value)
			s += '/tmp/'+filename
	
		
		return (status,response_headers, s + " saved")