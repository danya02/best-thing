from database import *
import json

def create(title, description, image=None):
    try:
        Thing.create(title=title, description=description, image=image)
    except IntegrityError:
        pass
data = json.load(open('taxons.json'))
for i in data:
    print(i['itemLabel'])
    create(i['itemLabel'], i['itemDescription'], i['img'])

