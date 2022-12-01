# talksql

## Examples

```python 
ipcfg = {
    'user': '',
    'password': '',
    'host': '',
	'db':'' }

cfg = { 'socket':"/tmp/mysql.sock",
    'user': '',
    'password': '',
    'host': '',
	'db':'' }

from talksql import *
con = ipconnect(ipcfg) #or
con = sockconnect(cfg)
#con is mysql connector connection object
```

## Get a resultset
```python 
from talksql import *
sql="select * from table where .." 
rs,c = xecrs(con,sql)
#rs is array for rows and columns of resultset
#c is cursor mysql connection 
# - go to mysql connector if you have to use the cursor to iterate
#this works unless you need to deal with large datasets
```

## Sub data and get a resultset
```python 
from talksql import *
sql="select * from table where column=%s"
data=(value,)
#data is %s sub-ed  
rs,c = xecrs(con,sql,data)
```

```python 
from talksql import *
sql="delete from table"
#data is %s sub-ed if given like resultset  
c = xec(con,sql)
#c is the cursor
```

## Few more 
sqlaofa, sqlaofd are experimental and only works as string data