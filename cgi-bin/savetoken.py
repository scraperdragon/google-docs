#!/usr/bin/python
import sys
import os
import requests
import json
import urlparse

def output(msg):
    print json.dumps(msg)
    exit(0)

print "Content-type: application/json\n\n"; 

params = urlparse.parse_qs(os.environ.get("QUERY_STRING"))
key, = params.get('key')

if not(key):
    output({"error": "no key"})
else:
    with open("/home/google_api_key.json", "w") as f:
        json.dump(key, f)
    output({"key": key})
