__author__ = 'yutongpang'
import os
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
mypath = BASE_DIR + '/database/main/Ag3AsS3/Hulme-e.yml'

with open(mypath) as f:
    doc = yaml.load(f)
    print(doc)
    doc['DATA'][0]['data'] = '0.00236 0.99667 0.00774\n0.00316 0.99770 0.00530\n'
    print(doc)

