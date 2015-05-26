__author__ = 'yutongpang'
import os
import yaml
import urllib2
from termcolor import colored

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
mypath = BASE_DIR + '/database/other/doped crystals'

from sqlalchemy.orm import sessionmaker
from sqlmap import db_connect, create_table, Elementlist, Element
from sqlalchemy import update
from sqlalchemy import and_

engine = db_connect()
create_table(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


def scrapdata(url):
    response = urllib2.urlopen(url)
    htmldata = response.read().replace(',', ' ')
    htmldata = htmldata.replace('\r', '')
    htmldata = htmldata.replace('wl n\n', '')
    return htmldata

element = 'Nb-RbTiOPO4'
title = 'Carvajal-gamma'
filepath = mypath + '/' + element + '/' + title + '.yml'
with open(filepath) as f:
    doc = yaml.load(f)
try:
    import time
    parentelement = session.query(Element).filter(Element.title == element).one()
    url = 'http://refractiveindex.info/tmp/other/doped%20crystals/Nb-RbTiOPO4/Carvajal-gamma.csv'
    print(element)
    try:
        dataexist = doc['DATA'][0]['data']
    except KeyError:
        data = scrapdata(url)
        doc['DATA'][0]['data'] = data
    stmt = update(Elementlist).where(and_(Elementlist.element == parentelement, Elementlist.title == title)). \
        values(data=doc)
    session.execute(stmt)
    session.commit()
    print('sucess')
except urllib2.HTTPError:
    print colored(element, 'red')
    print colored(title, 'red')
    print('\n')



