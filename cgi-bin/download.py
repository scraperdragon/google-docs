#!/usr/bin/python
import sys
import os
import requests
import json
import urlparse

def request_with_key(url):
    return requests.get(url, headers={'Authorization': 'Bearer {key}'.format(key=key)})

def output(msg):
    print json.dumps(msg)
    exit(0)

DRIVE_FILES_URL = "https://www.googleapis.com/drive/v2/files/{id}"
DOCUMENT_EXPORT_URL = "https://docs.google.com/feeds/download/documents/export/Export?id={id}&exportFormat={format}"

print "Content-type: application/json\n\n"; 

# acquire environment
if len(sys.argv) == 4:
    doc_id, key, filename = sys.argv[1:]
else:
    params = urlparse.parse_qs(os.environ.get("QUERY_STRING"))
    doc_id, = params.get('id')
    key, = params.get('key')
    filename, = params.get('filename')

if not(doc_id):
    output({"error": "no id"})
if not(key):
    output({"error": "no key"})
if not(filename):
    output({"error": "no filename"})

r = request_with_key(DRIVE_FILES_URL.format(id=doc_id))
try:
    j = r.json()
except Exception:
    output({"error": "response wasn't json", "error_detail":r.content, "params": params})

if 'downloadUrl' in j:
    xlsx_url = j['downloadUrl']
else: 
    xlsx_url = j['exportLinks']['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']

xlsx_content = request_with_key(xlsx_url).content
with open(filename, 'w') as f:
    f.write(xlsx_content)
output({"filename": filename})
