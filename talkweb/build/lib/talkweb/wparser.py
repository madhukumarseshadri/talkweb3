# # Copyright (c) Madhukumar Seshadri
## All rights reserved

class buff:
	""" stream buffer so you can say initialize, seek or mov to a point, tell  """

	def __init__(self, s):
		""" initaiize with python string """
		self.s = s
		self.i = -1
		self.len = len(s)

	def read(self):
		""" increments on ask so tell is not next pos of the char but exact pos of char given """
		self.i += 1
		if self.i < self.len:
			return self.s[self.i]

	def seek(self, n):
		""" set the pos within string """
		if n > 0:
			self.i = n - 1
		else:
			self.i = -1

	def tell(self):
		""" gives the exact pos where a char is """
		return self.i

	def mov(self, n):
		""" move n pos negative value moves to back till beginning of string, postive values moves forward till length of string """
		self.i = self.i + n
		if self.i < 0:
			self.i = -1
		if self.i > self.len:
			self.i = self.len


class wparser:
	def __init__(self, fn, fnis='s'):
		""" initialize with fn being string or filename, set fnis as 'f' for file or 's' for string esc is cls.esc """
		self.esc = "\\"
		self.w = '';
		self.prw = ''
		self.c = '';
		self.prc = ''
		self.wc = 0
		if fnis == "f":
			h = open(fn, "r")
			self.f = buff(h.read())
			h.close()
			return
		if fnis == "s":
			self.f = buff(fn)
		else:
			print ("error: unknown param. fn has to be a filename or buffer of chars")

	def nw(self):
		""" get next word """
		self.prc = self.c
		self.c = self.f.read()
		self.prw = self.w
		self.w = ''
		while (self.c):
			self.w = self.w + self.c
			if self.c in [' ', '\t', '\n']:  # and self.prc  s!=elf.esc:
				w = self.w[0:len(self.w) - 1]
				#print "self.w>"+"'" + self.w + "'" 			##- comment the if block below to take out <eol>
				#if self.c =='\n':
				#print "        nw>"+self.w
				#self.w = self.w[0:len(self.w)-1] #+ '<eol>'
				self.wc += 1
				return w
			self.prc = self.c
			self.c = self.f.read()
		if self.w == '':
			self.c = 'z'
			return None
		else:
			self.wc += 1
			self.c = 'z'
			return self.w

	def intel(self):
		"""  returns (wordcount,position of char where word was broken,char that broke word """
		return (self.wc, self.f.tell(), self.c)

	def mbw(self):
		"""   incomplete rewind - just moves offset - will not reset self.c, self.prc, self.w and self.pw """
		if self.w != None:
			self.f.mov((len(self.w) * -1) - 1)

	def _count(self, s):
		""" if you use wtc to get words till char, this is used keep the word count intact """
		for i in s:
			if i == ['\n', '\t', ' ']:
				self.wc += 1


	def wtc(self, c, esc):
		"""" returns string (words) till match of char given in c that is not escaped, if escaped, escaped char is removed
		     note - self.w is sequence broken no longer the word
		"""
		self.c = self.f.read()
		self.w = ''
		while (self.c):
			if self.c in c and self.prc != esc:
				break
			elif self.c in c and self.prc == esc:
				self.w = self.w[0:-1]

			self.w = self.w + self.c
			self.prc = self.c
			self.c = self.f.read()

		self._count(self.w)
		return self.w

	@classmethod
	def search(self, charset, s, start=0):
		for i, c in enumerate(s):
			if c in charset and i >= start:
				return (i, c)
		return (-1, 0)
