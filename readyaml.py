__author__ = 'yutongpang'
import os
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
mypath = BASE_DIR + '/database/main/Ag3AsS3/Hulme-e.yml'
import urllib2
response = urllib2.urlopen('http://refractiveindex.info/tmp/main/Ag3AsS3/Hulme-e.csv')
htmldata = response.read().replace(',', ' ')
htmldata = htmldata.replace('\r', '')
htmldata = htmldata.replace('wl n\n', '')

with open(mypath) as f:
    doc = yaml.load(f)
    print(doc)
    try:
        dataexist = doc['DATA'][0]['data']
    except KeyError:
        doc['DATA'][0]['data'] = htmldata
        print(doc)

