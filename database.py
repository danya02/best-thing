from peewee import *

db = MySQLDatabase('best', user='best', password='best', host='10.0.0.2')
db.connect()

class MyModel(Model):
    class Meta:
        database = db
