# Talkweb for python 3

A light weight server side framewok written in python to build web applications rapidly. 

It has three packages,
1) talkweb - package to convert html to objects and work on the object tree
2) wsgitalkback - write responders to url requests using this package
3) talksql - get your sql work quickly done

Installation

```
pip3 install talkweb
pip3 install wsgitalkback
pip3 install talksql
```

Download github and deploy by install modules separately and in shell,
```
python setup.py install from wsgitalkback directory
python setup.py install from talkweb directory
python setup.py install from talksql directory
```

## Talkweb
 
https://youtu.be/aDU1JluxNFU

## Talkback 

A responder framework to work with any wsgi (web server gateway interface). It uses cookie, query string, posted form data extractions in accordance to RFC 2616-hypertext transfer protocol and RFC 2965 that defines cookie protocols. It also implements a responder framework to respond to each http request and a session keeper to manage sessions.

### Pre-requiste 

You will need a web server and WSGI complaint interface
1)  https://httpd.apache.org/ 
2)  mod_wsgi https://pypi.org/project/mod-wsgi/, a WSGI https://www.python.org/dev/peps/pep-0333/ compliant interface for hosting python web based applications.

## Talksql

Get your sql work done quikcly. It is not needed to get examples app running. 

Example python script,

```python
ipcfg = {
    'user': '',
    'password': '',
    'host': '1',
    'db':'' }

cfg = { 'socket':"/tmp/mysql.sock",
    'user': '',
    'password': '',
    'db':'' }

con = ipconnect(ipcfg)
sql = "select * from sometable"
#xec/rs executes the sql and returns the rs in rs with cursor in c  
rs,c=xecrs(con,sql)
```

Pre-requiste

You will need mysql server,
1) mysql server https://www.mysql.com/downloads/ and 
2) mysql conector https://dev.mysql.com/downloads/connector/python/


## An example web app

If you have apache webserver and mod_wsgi installed, you can deploy the examples app. Just run the deploy shell script in examples folder after setting app name in deploy script. If you are going to use sql server as session store, then mysql server, mysql connector will need to be installed as well.

Configure gate.py as WSGIScriptAlias for the apache's httpd.conf,
```
WSGIScriptAlias /ex /usr/local/app/twexamples/gate.py
<Directory "/usr/local/app/twexamples">
Require all granted
</Directory>
```

You can view the example at
http://localhost/twexamples/helloworld.html

If you want to use the session in wsgitalkback for managing user sessions, you will need a table in your database for storing user sessions, schema is given below.

```
CREATE TABLE session (
  sessionid varchar(100) NOT NULL,
  obj blob,
  appname varchar(20) DEFAULT NULL,
  login tinyint(4) DEFAULT NULL,
  lastused datetime DEFAULT NULL
)
```

Lot more can be done.

* Talkweb can be made capable to handling css style querying of html elements like document.queryselector() or jquery's $().

Testing

* Packages are not tested for Windows and developed on Mac OS X. It should work on windows, there can some path issues, if found raise an issue in github. I don't have a windows setup to work on.

