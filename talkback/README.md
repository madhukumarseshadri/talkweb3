# talkback

Respond with your response to requests

## Use routes file to map url path to responders
See examples app in https://www.github.com/madhukumarseshadri/talkweb3

# Examples of GET / POST / PUT / DELETE

## Examples of managing formdata,

In the responder, self.qs is query string.

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
See examples app

## For PUT,
use self.processinput() within a responder 
## For DELETE 
use self.processinput() within a responder 

## OPTIONS / HEAD / CONNECT AND TRACE for http server to manage

### Examples for using session and cookies - see session.py in examples

fskeeper - keeps the sesson as file and pickles the session object to file
sqlkeeper - keepes the session in the database in session table 
