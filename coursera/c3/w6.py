import urllib.request as req, urllib.parse as parse
import json

base_url = 'http://py4e-data.dr-chuck.net/json?'
location = input('Enter location: ')
params = dict()
params["address"] = location
params['key'] = 42
url = base_url + parse.urlencode(params)
print('Retrieving ' + url)
res = req.urlopen(url)
print('Retrieved ' + res.headers["Content-Length"] + ' characters')
data = res.read()
try:
    js = json.loads(data)
except:
    js = None

if not js or 'status' not in js or js['status'] != 'OK':
        print('==== Failure To Retrieve ====')
        print(data)

print('Place id ' + js["results"][0]["place_id"])