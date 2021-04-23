# Examples app for Talkweb

You will need

1) Installed apache
2) Installed mod_wsgi and enabled the module in apache conf
3) pip3 or python setup.py install talkweb
4) pip3 or python setup.py install wsgitalkback
5) pip3 install talksql
6) mysql server if you are going to use session and created session table

Check README.md if you have not done above 

Edit the config.py in examples/responders to connect to your sql server

```python
ipcfg = {
    'user': '',
    'password': '',
    'host': '1',
    'db':'' } 
```

Run the deploy script in examples folder,

You see the examples app at
http://localhost/twexamples/helloworld.html

