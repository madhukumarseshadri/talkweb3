from talkweb import *
from wsgitalkback import *
import config

class myresponder(uiresponder):
	def manage_session(self):
		#centralize main session processing
		#you can do this inside responder as well
		usession=None
		
		#use type=mysql if you are keeping the session in db
		#import talksql to get the connection to db
		#con=ipconnect(config.ipcfg)
		#sk = sqlsessionkeeper(connection=con)
		sk = fskeeper(basedir=config.session_rootdir)

		cookies=html_cookies.fromrequest(self.environ)
		sessioncookie=None
		for acookie in cookies:
			if acookie.name == "TALKWEB_EXAMPLE":
				sessioncookie = acookie

		self.cookies = cookies
		
		if sessioncookie:
			usession = sk.get(sessioncookie.value)
			self.usession = usession

		self.response_headers=[]
		if not usession:
			usession = session()
			scookie = cookie("TALKWEB_EXAMPLE",usession.id)
			scookie.sethttponly()
			scookie.setsamesite("lax")
			sk.put(usession)
			self.usession = usession

			#scookie.setsecure()
			self.response_headers=html_cookies.toinject([scookie])

	def respond(self):
		status = "200 OK"

		self.manage_session()

		#application name
		an = appname(self.environ)
		#wsgi alias for application configured in apache conf
		wan = wsgialias(self.environ)
		#application base directory
		#abd = appbasedir(self.environ)

		#print to apache log
		#print('an',an,'wan',wan,'abd',abd)

		fn = self.appbasedir + os.sep + 'html' + os.sep + "helloworld.html"

		page = h2oo(fn)

		container = page.findcellbyid("helloworldcontainer")
		container.addcell(h2oo("""<div>Hello World! with Session. 
		See Server Code session.py in responders.</div>""",'s'))

		return (status,self.response_headers,page.html())



		