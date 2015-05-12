__author__ = 'yutongpang'
import os
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
mypath = BASE_DIR + '/database/other/other'

from sqlalchemy.orm import sessionmaker
from sqlmap import db_connect, create_table, Elementlist, Element
from .secret_key import access_key, secret_key
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import uuid

engine = db_connect()
create_table(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


def updatefiletos3(filepath):
    conn = S3Connection(access_key, secret_key)
    b = conn.get_bucket('refractiveindex')
    k = Key(b)
    k.key = uuid.uuid4()
    k.set_contents_from_filename(filepath)
    k.set_acl('public-read')
    return k.generate_url(expires_in=0, query_auth=False)


for element in os.listdir(mypath):
    newdir = mypath + '/' + element
    for elementlist in os.listdir(newdir):
        filepath = newdir + '/' + elementlist
        with open(filepath) as f:
            doc = yaml.load(f)
        datalink = updatefiletos3(filepath)
        title = elementlist.replace('.yml', '')
        parentelement = session.query(Element).filter(Element.title == element).one()
        try:
            references = doc['REFERENCES']
        except:
            references = ''
        try:
            comments = doc['COMMENTS']
        except:
            comments = ''
        datatype = doc['DATA'][0]['type']
        print(title)
        print(datalink)
        newelementlist = Elementlist(element=parentelement, title=title, references=references, comments=comments,
                                    type=datatype, datalink=datalink)
        session.add(newelementlist)
        session.commit()

