#!/usr/bin/python
import sys
import os
import requests
import json
import urlparse

def request_with_key(url):
    return requests.get(url, headers={'Authorization': 'Bearer {key}'.format(key=key)})

DRIVE_FILES_URL = "https://www.googleapis.com/drive/v2/files/{id}"

def download_xls(doc_id, filename):
    r = request_with_key(DRIVE_FILES_URL.format(id=doc_id))
    try:
        j = r.json()
    except Exception:
        output({"error": "response wasn't json", "error_detail":r.content, "params": params})
    
    if 'error' in j:
        print json.dumps(j, indent=2)
        raise RuntimeError

    elif 'downloadUrl' in j:
        xlsx_url = j['downloadUrl']
        #raise NotImplementedError("stopping for no reason, delete this line")
    elif 'exportLinks' in j:
        print j['exportLinks'].keys() 
        xlsx_url = j['exportLinks']['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
    else:
        print doc_id
    print xlsx_url

    xlsx_content = request_with_key(xlsx_url).content
    with open(filename, 'w') as f:
        f.write(xlsx_content)

def get_key():
    with open("/home/google_api_key.json") as f:
        return json.load(f)
key = get_key()

if __name__ == '__main__':
    for _id in open('/home/tool/swtime/ids.txt').read().strip().split('\n'):
        print repr(_id)
        download_xls(_id, "{}.xlsx".format(_id))
