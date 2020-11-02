from peewee import *

db = MySQLDatabase('best', user='best', password='best', host='127.0.0.1')

class MyModel(Model):
    class Meta:
        database = db

def create_table(table):
    db.create_tables([table])
    return table

@create_table
class Thing(MyModel):
    title = CharField(unique=True)
    description = TextField()
    image = CharField(null=True) # URL to image
    matchups = IntegerField(index=True)
    wins = IntegerField(index=True)
