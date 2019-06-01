import urllib.request as req, urllib.parse as parse
import xml.etree.ElementTree as ET

url = input('Enter localtion: ')
print('Retrieving ' + url)
res = req.urlopen(url)
print('Retrieved ' + res.headers["Content-Length"] + ' characters')
data = res.read()
tree = ET.fromstring(data)
counts = tree.findall('.//count')
print('Count: ' + str(len(counts)))
sum = 0
for count in counts:
    sum += int(count.text)
print('Sum: ' + str(sum))