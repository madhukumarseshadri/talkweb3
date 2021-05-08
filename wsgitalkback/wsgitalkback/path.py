"""
path.py 
Author - Madhukumar Seshadri
Copyright(c) Madhukumar Seshadri
Purpose: path components
"""
import os
import re
import time

def createdir(adir):
	""" create dir if not exists """
	try: 
		os.stat(adir)
	except:
		os.mkdir(adir)
		try:
			os.stat(dir)
		except:
			return
	return adir

def pathfile(apath):
	""" it assumes at the last os.extpath (dot in the case of posix)
		to be the extension everything before till last os.sep will 
		become the filename """
	path="";fn=""
	pieces=apath.split(os.sep)
	pathpieces=pieces[:-1]
	for one in pathpieces:
		path += one + os.sep
	
	tfn=pieces[-1:]
	if type(tfn) is list:
		for i in tfn:
			fn += i
	else:
		fn = tfn

	return (path,fn)

def pathfileext(apath):
	""" it assumes at the last os.extpath (dot in the case of posix)
		to be the extension everything before till last os.sep will 
		become the filename """
	path="";fn="";ext=""
	pieces=apath.split(os.sep)
	pathpieces=pieces[:-1]
	for one in pathpieces:
		path += one + os.sep
	
	tfn=pieces[-1:]
	if type(tfn) is list:
		for i in tfn:
			fn += i
	else:
		fn = tfn

	extpieces=fn.split(os.extsep)
	if len(extpieces) > 1:
		#atleast there are two pieces separated by os.extsep
		fnn=extpieces[:-1]
		fn=""
		for one in fnn:
			fn += one + os.extsep
		fn = fn[0:-1]

		ext=extpieces[-1:]

	if fn:
		return (path,fn,ext)

def pathpieces(apath):
	""" incase of posix first one will be empty space
	as root is mounted as os.sep, last parameter in return is os separator """
	return (apath.split(os.sep),os.sep)

def filesusingfilter(dir,exp=".+"):
	""" dir is path and exp is the filter that confines to re patterns"""
	output=[]
	for dirpath,dirnames,files in os.walk(dir):
		for x in files:
			if re.match(exp,x):
				#output.append(dirpath+"/"+x)
				output.append([x,os.stat(dirpath+os.sep+x)])
	return output

def filesindirusingfilter(dir,exp=".+"):
	""" dir is path and exp is the filter that confines to re patterns"""
	output=[]
	for afile in os.listdir(dir):
		if re.match(exp,afile):
			#output.append(dirpath+"/"+x)
			output.append([afile,os.stat(dir + os.sep + afile)])
	return output

def filesinpathusingfilter(dir,exp=".+"):
	""" dir is path and exp is the filter that confines to re patterns"""
	output=[]
	for afile in os.listdir(dir):
		if re.match(exp,afile):
			#output.append(dirpath+"/"+x)
			output.append([dir+os.sep+afile,os.stat(dir + os.sep + afile)])
	return output


def lastaccess(filestat):
	"""filestat is posix filestat given to using python os package type posix.stat_result"""
	return time.ctime(filestat.st_atime)

def lastchanged(filestat):
	"""filestat is posix filestat given to using python os package type posix.stat_result"""
	return time.ctime(filestat.st_ctime)
	
def lastmodified(filestat):
	"""filestat is posix filestat given to using python os package type posix.stat_result"""
	return time.ctime(filestat.st_mtime)

"""
def user(filestat)
def group(filestat)
def device(filestat)
def inode(filestat)
"""
def cutoff(something,fromsomething):
	return re.subn(something,"",fromsomething)


""" from mask.py in pylib .. """
prefix="posix:"
prefix=""

fs_mode_mask=61440 		#0170000
fsnodetypes={16384:prefix+"d",\
		8192:prefix+"c",\
		24576:prefix+"b",\
		32768:prefix+"r",\
		4096:prefix+"f",\
		40960:prefix+"l",\
		49152:prefix+"s"}
"""d is dir / c = chardevice / b is blockdevice
	r is regularfile / f is fifo / l is link / s is socket """

def reverse(s):
	""" reverse a damn string """
	rs=""; l = len(s);
	while l > 0:
		rs += s[l-1]
		l -= 1
	return rs

def toint(binstr):
	""" it returns binstr as is """
	astr = binstr[2:]
	v=0;n=0;
	astr = reverse(astr)
	for adigit in astr:
		v += int(adigit) * (2**n)
		n +=1
	return v

def intmask(anint, maskint):
	""" binstr of int and binstr of mask 
		pathetic number of reverses .. change to run in reverse 
	"""
	i1=bin(anint)[2:]
	m=bin(maskint)[2:]

	i1l=len(i1); ml=len(m);
	
	#print ("given integer is ..",anint, i1, "toint of that is",toint(bin(anint)))
	#print ("given mask is ..",maskint, m, "toint of that is",toint(bin(maskint)))

	retstr=""

	anint_range=range(i1l)
	m_range=range(ml)
	anint_range.reverse()
	
	for i in anint_range:
		v = i1[i]
		if i in m_range:
			corresponding_maskbit=m[i]
		else:
			corresponding_maskbit=0

		if corresponding_maskbit == "1":
			retstr += v
		else: 
			retstr += "0"

	retstr = reverse(retstr)
	#print ("masked result in str ..",retstr)
	return toint("0b"+retstr)

def filetype(fstat):
	postmask=intmask(fstat.st_mode,fs_mode_mask)
	if postmask in fsnodetypes:
		return fsnodetypes[postmask]

import sys	
if __name__=="__main__":
	#print (pathfileext("/home/madhu/Desktop/x.y~"))
	#print (pathfileext("/home/madhu/Desktop/x.y.z"))
	target="."
	if len(sys.argv):
		target = sys.argv[1]
	for a in os.listdir(target):
		print (a,filetype(os.stat(target+"/"+a)))
