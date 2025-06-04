# Talkweb for python 3

A python web framework for building web applications rapidly. 

It has three packages,
1) talkweb - package to convert html to objects and work on the object tree
2) talkback - write responders to url requests using this package
3) talksql - get your sql work quickly done, use the code inside for managing the connector

Installation

```
pip3 install talkweb
pip3 install talkback
pip3 install talksql
```

Download github and deploy by install modules separately and in shell,
```
python setup.py install from talkback directory
python setup.py install from talkweb directory
python setup.py install from talksql directory
```

## Why Talkweb?

https://www.madhu.tokyo/blog/software/why-talkweb-for-python-web-development/

## Talkweb

Assemble using Templates or Objects - Talkweb says Objects

Talkweb makes a Object tree of html and allows insertion of other htmls into the tree. 

```python
from talkweb import *
roots = h2o(htmlfile)
#assuming htmlfile has &lt;!Doctype html&gt;&lt;html&gt;&lt;div id="x"&gt;&lt;/div&gt;&lt;/html&gt;

#cell is a node
roots[1].findcellbyid("x") 
widget = h2o(widgethtmlfile)
roots[1].addcell(widget)

html=''
for root in roots:
    html += root.html()
print(html)
```

Like it, then you will like to develop with talkweb. If not, leave you to templates and it's rules.

https://www.youtube.com/watch?v=Dh000mkLYSI

## Talkback 

A responder framework to work with any wsgi (web server gateway interface). It uses cookie, query string, posted form data extractions in accordance to RFC 2616-hypertext transfer protocol and RFC 2965 that defines cookie protocols. It also implements a responder framework to respond to each http request and a session keeper to manage sessions.

## Building a web app 

To get started quickly use wsgi_ref https://docs.python.org/3/library/wsgiref.html. 

```python
python wsgi.py #in examples folder
```
https://www.youtube.com/watch?v=bk5Bjaa4HHo

### Pre-requiste to deploy with Apache httpd

On linux, you can use apt,
```shell
sudo apt install python3-pip
sudo apt install apache2
sudo apt install libapache2-mod-wsgi-py3
```
You will need a web server and WSGI complaint interface
1)  https://httpd.apache.org/ 
2)  mod_wsgi https://pypi.org/project/mod-wsgi/, a WSGI https://www.python.org/dev/peps/pep-0333/ compliant interface for hosting python web based applications.

## Talksql

Get your sql work done quickly. It is not needed to get examples app running. 

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
On linux, you can use apt, 
```shell
sudo apt install mysql-server
pip install mysql-connector
```

You will need mysql server,
1) mysql server https://www.mysql.com/downloads/ and 
2) mysql conector https://dev.mysql.com/downloads/connector/python/


## An example web app for examples

If you have apache webserver and mod_wsgi installed, you can deploy the examples app. Just run the deploy shell script in examples folder after setting app name in deploy script. If you are going to use sql server as session store, then mysql server, mysql connector will need to be installed as well.

Configure gate.py as WSGIScriptAlias for the apache's httpd.conf,
```
WSGIScriptAlias /ex /usr/local/app/twexamples/gate.py
<Directory "/usr/local/app/twexamples">
Require all granted
</Directory>
```

You can view the example at
http://localhost/twexamples/

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

Testing

* Packages are not tested for Windows and developed on Mac OS X. It should work on windows, there can some path issues, if found raise an issue in github. I don't have a windows setup to work on.
* It's not perfect but stable and working well for web apps, issues, problems, features - create them in this repository, so they can fixed or added. 


