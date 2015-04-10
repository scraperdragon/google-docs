#!/usr/bin/python
import sys
import os
import requests
import json
import urlparse

print "Content-type: text/html\n\n"; 

params = urlparse.parse_qs(os.environ.get("QUERY_STRING"))
key, = params.get('key')

if not(key):
    print "<html><body><h1>No key</h1></body></html>"
    exit(1)
else:
    with open("/home/google_api_key.json", "w") as f:
        json.dump(key, f)
    print """ <html>    
  <head>      
    <title>Saved key: redirecting</title>      
    <meta http-equiv="refresh" content="0;URL='fullprocess'" />    
  </head>    
  <body> 
    <p>saved key: processing... should be refreshing, otherwise try <a href='fullprocess'>fullprocess</a></p> 
  </body>  
</html>     """
    exit(0)
