""" cell (html element)
purpose - come to cell from html
author -- Madhukumar Seshadri
copyright -- All rights reserved to Madhukumar Seshadri
license -- see copyright
"""
class style(object):
	def html(self):
		return ""

class cell(object):
	def __init__(self,tag="div",startendtogether=False):
		self.tag=tag
		self.attr=[]
		self.listofcells=[]
		self.parent = None
		self.startendtogether = startendtogether
		self.elementcell=True
		self.styleattrib=style()
		self.data=''
		self.output={}

	def __str__(self):
		return self.html()

	def __len__(self):
		return len(self.listofcells)

	def settag(self,tag):
		self.tag=tag

	def parentcell(self):
		return self.parent

	def attrib(self,name):
		for k,v in self.attr:
			if k == name:   return v

	def addattrib(self,name,value=None):
		for i,kv in enumerate(self.attr):
			if kv[0] == name:
				self.attr[i]=[name,value]
				return
		self.attr.append([name,value])

	def removeattrib(self,name):
		for i,kv in enumerate(self.attr):
			if kv[0] == name:
				del self.attr[i]

	def _data(self):
		self.output['data'] = self.data

	def _htmlcss(self):
		""" assembles the html css for this cell """
		self.output['style']=self.styleattrib.html()

	def _htmlc(self):
		""" assembles the closing html tag for this cell """
		return "</" + self.tag + ">"

	def _html(self):
		""" assembles the complete html for this cell """
		self._data()
		self._htmlcss()
		style = self.output['style']
		data = self.output['data']
		output = '<' + self.tag + " "
		for k,v in self.attr:
			#print k,v
			if k and v:
				output += k + "=" + '"' + v + '" '
			else:
				output += k + ' '
		output = output[:-1]
		if style.strip() != '':
			output = output + ' style="' + style + '"'
		output += ">"
		self.output={}
		return (output,data)

	def htmlgen(self,onecell,output=[]):
		""" generates html for the cell and all it's belongings output is output list"""
		otag,contents=onecell._html()
		if otag is None:
			output.append([0,None,contents])
			return

		if onecell.startendtogether:
			otag = otag[:-1] + "/>"
			output.append([1,otag,contents])
			return

		output.append([1,otag,contents])

		for acell in onecell.listofcells:
			self.htmlgen(acell,output)

		output.append([0,onecell._htmlc(),""])

	def html(self):
		htmllist=[]
		self.htmlgen(self,htmllist)
		return self.tostr(htmllist)

	def formattedhtml(self):
		htmllist=[]
		self.htmlgen(self,htmllist)
		return self.toformattedstr(htmllist)

	def toformattedstr(self,agenlist):
		""" tostr from agenlist from nhgen or htmlgen """
		s="";
		padding=-1;
		for tagtype,tag,contents in agenlist:
			if tag is None:
				s += contents
				continue
			if tagtype:
				#openings
				if tag.lower() == "<pre>":
					s += self.pad(padding) + tag + contents
					continue
				padding += 1
				s += self.pad(padding) + tag + "\n"
				pv=self.pad(padding+1)
				if contents and contents.strip():
					for aline in contents.split("\n"):
						if aline.strip():
							s += pv + aline + "\n"
			else:
				#closing
				s += self.pad(padding) + tag + "\n"
				padding -= 1

		return s[0:-1]

	def tostr(self,agenlist):
		""" tostr from agenlist from nhgen or htmlgen """
		s="";
		for tagtype,tag,contents in agenlist:
			if tag is None:
				s += contents
				continue
			if tagtype:
				s += tag + contents
			else:
				s += tag
		return s

	def attribsearch(self,key,value=None):
		for k,v in self.attr:
			if k==key and v==value:
				return True

	def _findcellusingid(self,findthis,within,match=[]):
		""" findthis-cellid, within which cell and match is output """
		if self.attribsearch('id',findthis):
			match.append(self)
			return
		for i,acell in enumerate(within.listofcells):
			if not acell.elementcell:   continue
			if acell.attribsearch('id',findthis):
				match.append(acell)
				return acell;
			else:
				if len(acell.listofcells) > 0:
					self._findcellusingid(findthis,acell,match)

	def findcellbyid(self,findthis):
		""" findcellusingid using identifier provided as first arg to this """
		match=[]
		self._findcellusingid(findthis,self,match)
		if len(match) > 0:
			return match[0]
		else:
			return None

	def findcellusingid(self,findthis):
		""" findcellusingid using identifier provided as first arg to this """
		match=[]
		self._findcellusingid(findthis,self,match)
		return match

	def _findcellusingtag(self,findthis,within,match=[]):
		""" findthis-celltype, within which cell and match is output """
		#match.append(len(match) + 1)
		for i,acell in enumerate(within.listofcells):
			if acell.tag == findthis:
				match.append(acell)
				return acell;
			else:
				self._findcellusingtag(findthis,acell,match)

	def findcellbytagname(self,findthis):
		""" findcellusingtype using celltype (div / html or script) provided as first arg to this """
		match=[]
		self._findcellusingtag(findthis,self,match)
		return match

	## section -- builders -- for adding / removing
	def addcell(self,incoming):
		""" add to this cell """
		acell=incoming
		if type(incoming) in [str,float,int]:
			acell = cell(str(incoming))
		acell.parent=self
		self.listofcells.append(acell)
		return acell

	def addcellundercell(self,cellid,acell):
		""" cellid is idofcell under which acell need to be added  """
		x=self.findcellusingid(cellid)
		if len(x) > 0:
			#acell.parent=x[0]
			x[0].addcell(acell)
			return x[0]

	def addcellbeforecell(self,cellid,acell):
		""" cellid is idofcell under which acell need to be added  """
		x=self.findcellusingid(cellid)
		if len(x) > 0:
			#print "found",x[0].id,x[0].parent
			if not x[0].parent:
				print("cell is root or does not have parent")
				return
			x[0].parent.insertcell(cellid,acell)
			return x[0]

	def insertcell(self,cellid,incoming):
		""" add to this cell """
		mylen = len(self.listofcells)
		acell=incoming
		if type(incoming) in [str,float,int]:
			acell = cell(str(incoming))
		hole=-1
		for i,xcell in enumerate(self.listofcells):
			#print i,xcell.id,cellid
			if xcell.attribsearch('id',cellid):
				#print "found cell ..",xcell
				hole=i
				self.listofcells.append(self.listofcells[mylen-1])
				arange = list(range(mylen))[i+1:]
				arange.reverse()
				for x in arange:
					self.listofcells[x]=self.listofcells[x-1]
				break;
		if (hole != -1):
			self.listofcells[hole]=acell
			acell.parent=self
			return acell

	def removecells(self,listofcells):
		 #remove a particular set within doted cell upon which I'm called, if empty, remove all cells
		removed=[]
		everything=len(listofcells)
		for i,acell in enumerate(self.listofcells):
			if not everything:
				removed.append(self.listofcells.pop(i))
			elif acell in listofcells:
				removed.append(self.listofcells.pop(i))
		return removed

	def removecell(self,cellid):
		cells = self.findcellusingid(cellid)
		for acell in cells:
			if acell.parent != None:
				acell.parent.removecells([acell])

	def removenthcell(self,n):
		""" n is nth cell within list """
		self.listofcells.pop(n)

	def pad(self,pad=0):
		x="";
		for i in range(pad):
			x += self.padsize
		return x

	def traverser(self):
		""" provides a list of cells """
		amap=[]
		self.traverse(self,amap)
		return amap

	def traverse(self,acell,result=[]):
		""" traverser """
		result.append(acell)
		for obj in acell.listofcells:
			self.traverse(obj,result)

class textcell(cell):
	def __init__(self,data):
		cell.__init__(self)
		self.data = data
		self.textcell=True

	def _html(self):
		return (None,self.data)

	def html(self):
		return self.data

class entityrefcell(cell):
	def __init__(self,data):
		cell.__init__(self)
		self.data=data
		self.entityrefcell=True

	def _html(self):
		return (None,'&'+self.data+';')

	def html(self):
		return '&'+self.data+';'

class charrefcell(cell):
	def __init__(self,data):
		cell.__init__(self)
		self.data=data
		self.charrefcell=True

	def _html(self):
		return (None,'&#'+self.data+';')

	def html(self):
		return '&#'+self.data+';'

class picell(cell):
	def __init__(self,data):
		cell.__init__(self)
		self.data=data
		self.picell=True
	def _html(self):
		return (None,"<?" + self.data + ">")
	def html(self):
		return "<?" + self.data + ">"

class commentcell(cell):
	def __init__(self,data):
		cell.__init__(self)
		self.data=data
		self.commentcell=True
	def _html(self):
		return (None,"<!--" + self.data + "-->")
	def html(self):
		return "<!--" + self.data + "-->"

class declcell(cell):
	def __init__(self,data):
		cell.__init__(self)
		self.data=data
		self.declcell=True
	def _html(self):
		return (None,"<!"+self.data+">")
	def html(self):
		return "<!"+self.data+">"

""" def removecells(self,listofcellids=[]):
		 #remove a particular set within doted cell upon which I'm called, if empty, remove all cells
		removed=[]
		everything=len(listofcellids)
		for i,acell in enumerate(self.listofcells):
			if not everything:
				removed.append(self.listofcells.pop(i))
			elif acell in listofcells:
				removed.append(self.listofcells.pop(i))
		return removed """
