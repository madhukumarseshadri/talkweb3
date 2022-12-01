# Examples

```python
python wsgi.py
```
or
Set the appname in deploy script before running it
Setup up with Apache

Configure gate.py as WSGIScriptAlias for the apache's httpd.conf,
```
WSGIScriptAlias /ex /usr/local/app/twexamples/gate.py
<Directory "/usr/local/app/twexamples">
Require all granted
</Directory>
```

