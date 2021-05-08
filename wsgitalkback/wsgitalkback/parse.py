"""
parse.py
Author - Madhukumar Seshadri
Copyright (c) Madhukumar Seshadri
"""
class bparser:
	esc=b'\\'
	whitespace=b' '
	newline=b"\n"
	tab=b"\t"
	wb=whitespace+newline+tab
	eol='eol'
	
	@classmethod
	def parse(cls,bytes_,start,l,breakers=wb):
		brokeon=None;prc=c=b''
		sequence=bytearray()
		i=start+1
		#print ("bparser:bparse>","start:",start,"length:",l,"breakers:",breakers)
		while i < l:
			c = bytes_[i]
			if c in breakers:
				output=(bytes(sequence),c,i)
				brokeon=c
				break
			else:
				sequence.append(c)
				i += 1
		if not brokeon:
			output=(bytes(sequence),cls.eol,i)
			#print ("bparser:bparse>output",output)
		return output

class multipart_parser:
	eol='eol'

	@classmethod
	def parse(cls,bytes_,start,l):
		brokeon=None;prc=c=b''
		sequence=bytearray()
		i=start+1
		#print ("bparser:bparse>","start:",start,"length:",l)
		while i < l:
			c = bytes_[i]
			if c == b'\n'[0] and prc == b'\r'[0]:
				brokeon=b'\r\n'
				slash_r=None
				output=(bytes(sequence[:-1]),brokeon,i)
				break
			elif c == b":"[0]:
				brokeon=b':'
				output=(bytes(sequence),brokeon,i)
				break
			prc = c
			sequence.append(c)
			i += 1
		if not brokeon:
			output=(bytes(sequence),cls.eol,i)
			#print ("bparser:bparse>output",output)
		return output

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
	def parse(cls,text,start,l,breakers):
		""" parse the text for breakers from start to l and
			return till breaker, broken char or cls.eol and index of break
			"""
		brokeon=None
		c=sequence=""
		i=start+1
		#print ("cparser:cparse>","input:",text,"start:",start,"length:",l,"breakers:",breakers)
		while i < l:
			c = text[i]
			if c in breakers:
				output=(sequence,c,i)
				brokeon=c
				break
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


if __name__ == "__main__":
	#x = b'madhu \t\n \m\\t <'
	#print('input is:',x,'breakers:',bparser.wb)
	#seq,b,i=bparser.parse(x,-1,len(x),bparser.wb)
	#while b is not bparser.eol:
	#    print(seq,b,i)
	#    seq,b,i=bparser.parse(x,i,len(x),bparser.wb)
	#print(seq,b,i)
	fn = "/Users/madhuseshadri/Desktop/s_4908_1.jpg"
	f = open(fn,"rb")
	x=f.read()
	w,b,i = multipart_parser.parse(x,-1,len(x))
	while b is not multipart_parser.eol:
		print(w,b,i)
		inp = input()
		w,b,i = multipart_parser.parse(x,i,len(x))
	print(w,b,i)
