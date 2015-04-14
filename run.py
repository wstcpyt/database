__author__ = 'yutongpang'
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
mypath = BASE_DIR + '/database/other/other'
print(os.listdir(mypath))

from sqlalchemy.orm import sessionmaker
from sqlmap import db_connect, create_table, Category, Element

engine = db_connect()
create_table(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
maincategory = session.query(Category).filter(Category.title == 'other').one()

for element in os.listdir(mypath):
    newelement = Element(title=element, category=maincategory)
    session.add(newelement)
    session.commit()