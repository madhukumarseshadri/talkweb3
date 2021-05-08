""" 
loader.py
Author : Madhukumar Seshari
Copyright (c) Madhukumar Seshadri
Purpose: loads a python module
""" 

import imp
import sys

class _x:
	emptyclass=""

def hunt(s,p=None):
	a="m"
	if p:
		sys.path.append(p)
	f,fn,smt=imp.find_module(s,None)
	if not f and fn:
		try:
			f = open(fn +".py","r")
		except IOError as e:
			#print ("tried to find as module:error",e)
			try:
				f = open(fn+"/__init__.py","r")
				a="p"
			except IOError as e:
				#print ("trying as package: erorr ",e)
				a=None

	return (a,f,fn,smt)
				
def live(s,p=None):
	""" where is s is string name of module"""
	m=None
	a,b,c,d=hunt(s,p)
	if a:
		m=imp.load_module(s,b,c,d)
		#f=open("/tmp/a.log","w")
		#f.write(str(m))
		#f.close()
		return m

def findclass(m,udef):
	""" find a class which is name of class in string loaded in udef in a live module """
	#print ("+ find class:",m,udef)
	for n in m.__dict__:
		if n in ["__builtins__","__file__","__package__"]:	continue
		o=m.__dict__[n]
		t=type(o)
		#print ("- iterating module:",n,o,t)
		if t is type or t is type(_x):
			if udef == o.__name__:
				return o

def findmydescendents(m,base,udef=None):
	""" find classes that are descendents of base 
			(my stands for all class needs to have __inheritances__ list loaded)
		given 
			a live module (load using live or pointer to modules in sys.modules)
			base is str of base class
			udef id str of class that is descendent of base
	"""
	out=[]
	#print ("+ finding class:",m,base,udef)
	for n in m.__dict__:
		if n in ["__builtins__","__file__","__package__"]:	continue
		o=m.__dict__[n]
		t=type(o)
		#print ("- iterating module:",n,o,t)
		if t is type or t is type(_x):
			metafound=0
			if "__inheritances__" not in o.__dict__:
				continue
			for one in o.__inheritances__:
				if base == one.__name__:
					metafound=1
			if metafound:
				if udef:
					if udef == o.__name__:
						out.append(o)
			else:
					out.append(o)

	return out

def instanceof(classobj,p=[]):
	""" given a class object, let there be one of that with a name that is randomly selected """
	syb="i"+str(1)
	#type.__new__(meta,classname,supers,classdict)
	syb=type.__new__(classobj,syb,(),{})
	#classobj.__setattr__(ahash,"nameofattribute",itsvaliue)
	return syb

"""
@possibilities - module inspector
def inspect(m):
	#pass the module in sys.module
	intriniscs=[int,float,str,list,dict,tuple]
	sybtype=type(syb)
	if sybtype in instriniscs:
		
	elif sybtype is "classobj":
		
	elif sybtype is "type":
		
	elif sybtype is "function":
		
class a(type):
	def __init__(self):
		print ("x","super")
	def am1(self):
		print ("am1")

class d(a):
	def __new__(cls):
		super(d,cls).__new__()

class x:
	__x__=""

y=type(x)("y",(x,),{})	#type(x) resolves to classobj
"""
