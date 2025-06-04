""" 
loader.py
Author : Madhukumar Seshari
Copyright (c) Madhukumar Seshadri
Purpose: loads a python module
""" 

import importlib
import sys

class _x:
	emptyclass=""

def hunt(s,p=None):
	a="m"
	if p:
		sys.path.append(p)
	f,fn,smt=importlib.find_module(s,None)
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
	m=importlib.import_module(s,p)
	#f=open("/tmp/a.log","w")
	#f.write(str(m))
	#f.close()
	return m


def instanceof(classobj,p=[]):
	""" given a class object, let there be one of that with a name that is randomly selected """
	syb="i"+str(1)
	#type.__new__(meta,classname,supers,classdict)
	syb=type.__new__(classobj,syb,(),{})
	#classobj.__setattr__(ahash,"nameofattribute",itsvaliue)
	return syb


