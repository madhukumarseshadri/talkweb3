## Talkweb

Assemble pages.

Talkweb makes a Object tree of html and allows addition, insertion and deletion to the tree like DOM.  

```python
from talkweb import *
roots = h2o(htmlfile)
#assuming htmlfile has <!Doctype html><html><div id="x"></div></html>

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
