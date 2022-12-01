# wsgitalkback

## Why not use routes for maping urls to path of responders?

I think you can simply use the url for getting the responder for the request, this way you don't need another configuration file for map or urls. http://localhost/appname?r=respondername&rest_of_querystring. If you purely think of PUT / DELETE / POST in http server world, it make sense to have routes but they anyway get mapped to script (responder), so we are getting away without mapping. Issue in in GET, r needs to be an hidden input in form, with this type of getting to the responders. This works fine except for hidden input for get, so one of these days, we will add route.py to avoid this hidden input in GET.

# Examples of GET / POST / PUT / DELETE

## Examples of managing formdata,

In the responder, self.qs is python string. self.qsaofa is array of array of qs vars.

## For GET / POST, form submission html forms,

use 
```python 
self.processform()
``` 
in the responder to get the formdata [ url encoded or multipart or text/plain ]

After using processform, self.formdata.data is,

For GET, 
self.formdata.data is a dict of field names, value pairs and field name and values are python strings and percent decoded and plus sub-ed. Get the form values as shown below, 

```python
type,fieldvalue,filename,content_type=self.formdata.data['fieldname'] #or
type,fieldvalue,filename,content_type=self.formdata['fieldname']
#type - empty or b'f' with f denoting input is file
#fieldvalue -  contents of file as bytes or field value
#filename - name of the file if file
#content_type - content_type of file if file 
```

For POST,
self.formdata.data - dict is byte field name value pairs if post is mutlipart/formdata
For url encoding posts, default encoding is utf8 no need to provide, provide python supported encoding or none for bytes in self.processforms(encoding=None). For utf8, values are percent decoded and plus sub-ed

```python
type,fieldvalue,filename,content_type=self.formdata.data['fieldname'] #or
type,fieldvalue,filename,content_type=self.formdata['fieldname']
```

For multipart/formdata with files, 
```python
type,fieldvalue,filename,content_type=self.formdata.data[b'fieldname'] or
type,fieldvalue,filename,content_type=self.formdata[b'file']
for type,fieldvalue,filename,content_type in self.formdata[b'files']:
	#input is multiple files
```

## AJAX formdata GET and POST

### GET / POST forms 

AJAX form data serialized as url-encoded,

```python
self.processform()
self.formdata.data 
#as GET/POST form above
```

AJAX form multipart/formdata,
```python
self.processform()
#as POST form for multipart above  
```

AJAX JSON.Stringify()

```python
input_bytes = self.processinput()
import json 
json.loads(input_bytes)
```

You cannot do self.processinput() and then call self.processform() as it reads
all of environ[wsgi.input]

All GET / POST for form submit are in examples, run the examples app and see client and server code. 

## For PUT,
use self.processinput() within a responder 
## For DELETE 
use self.processinput() within a responder 

## OPTIONS / HEAD / CONNECT AND TRACE for http server to manage

### Examples for using session and cookies - see session.py in examples

fskeeper - keeps the sesson as file and pickles the session object to file
sqlkeeper - keepes the session in the database in session table 
if you are implementing your own session keeper like redis or network file, then use the interface of session.py 

That wraps up the wsgitalkback package.