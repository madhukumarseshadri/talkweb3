""" cell (html element)
purpose - come to cell nh tag
author -- Madhukumar Seshadri
copyright -- All rights reserved to Madhukumar Seshadri
license -- see copyright
"""
from .cell import *
from html.parser import HTMLParser
#from htmlentitydefs import name2codepoint

def h2o(x,inputis='f'):
	s=''
	if inputis=='f':
		f = open(x,'r')
		s = f.read()
		f.close()
	else:
		s=x
	htoc = htmltocell()
	return htoc(s)

def h2oo(x,inputis='f'):
	o = h2o(x,inputis)
	if len(o) > 0:
		return o[0]

class htmltocell(HTMLParser):
	def __init__(self,convert_charrefs=False):
		HTMLParser.__init__(self,convert_charrefs=convert_charrefs)
		self.activecell = None
		self.output=[]

	def __call__(self,data):
		self.feed(data)
		return self.output

	def handle_starttag(self, tag, attrs):
		#print ("starttag>",tag,attrs,self.output)
		thiscell = cell(tag=tag)
		if self.activecell is None:
			self.output.append(thiscell)
			self.activecell = self.output[len(self.output)-1]
		else:
			self.activecell=self.activecell.addcell(thiscell)
		for k,v in attrs:
			self.activecell.addattrib(k,v)

	def handle_endtag(self, tag):
		#print ("endtag>",tag)
		self.activecell = self.activecell.parent

	def handle_data(self, data):
		#print ("data>",data.strip())
		if self.activecell is None:
			self.output.append(textcell(data))
		else:
			self.activecell.addcell(textcell(data))
			#self.activecell.data = data

	#def get_starttag_text(self):
		#print "start tag text"
		#pass

	def handle_startendtag(self,tag, attrs):
		#print "handle_startendtag",tag,attrs
		thiscell = cell(tag=tag,startendtogether=True)
		for k,v in attrs:
			thiscell.addattrib(k,v)
		if self.activecell is None:
			self.output.append(thiscell)
		else:
			self.activecell.addcell(thiscell)

	def handle_entityref(self,name):
		#print ('handle_entityref',name)
		self.activecell.addcell(entityrefcell(name))

	def handle_charref(self,name):
		#print ('handle_charref',name)
		self.activecell.addcell(charrefcell(name))

	def handle_comment(self,data):
		#print 'handle_cmment',data
		if self.activecell is None:
			self.output.append(commentcell(data))
		else:
			self.activecell.addcell(commentcell(data))

	def handle_decl(self,decl):
		#print ('handle_decl',decl)
		if self.activecell is None:
			self.output.append(declcell(decl))
		else:
			self.activecell.addcell(declcell(decl))

	def handle_pi(self,data):
		#print ('handle_pi',data)
		if self.activecell is None:
			self.output.append(picell(data))
		else:
			self.activecell.addcell(picell(data))
