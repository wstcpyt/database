__author__ = 'yutongpang'
import os
import yaml
import urllib2
from termcolor import colored



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
mypath = BASE_DIR + '/database/other/other'

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

for element in os.listdir(mypath):
    newdir = mypath + '/' + element
    for elementlist in os.listdir(newdir):
        filepath = newdir + '/' + elementlist
        with open(filepath) as f:
            doc = yaml.load(f)
        title = elementlist.replace('.yml', '')
        try:
            import time
            time.sleep(1)
            parentelement = session.query(Element).filter(Element.title == element).one()
            url = 'http://refractiveindex.info/tmp/other/' + element + '/' + title.replace(' ', '%20') + '.csv'
            print(element)
            try:
                dataexist = doc['DATA'][0]['data']
            except KeyError:
                data = scrapdata(url)
                doc['DATA'][0]['data'] = data
            stmt = update(Elementlist).where(and_(Elementlist.element == parentelement, Elementlist.title == title)).\
                values(data=doc)
            session.execute(stmt)
            session.commit()
        except urllib2.HTTPError:
            print colored(element, 'red')
            print colored(title, 'red')
            print('\n')



