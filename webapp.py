from database import *
from flask import Flask, request, render_template
import random

app = Flask(__name__)

def choose_thing(exclude=[]):
    thing = None
    max_id = Thing.select(fn.Max(Thing.id)).scalar()
    while thing is in [None]+exclude:
        thing = Thing.select().where(Thing.id >= random.randint(0, max_id))
    return 

class Null:
    pass

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        my = int(request.form['my-id'])
        other = int(request.form['other-id'])
        Thing.update(Thing.matchups == Thing.matchups+1).where(Thing.id._in([my, other])).execute()
        Thing.update(Thing.wins == Thing.wins + 1).where(Thing.id == my).execute()
        my = Thing.get(Thing.id == my)
        other = Thing.get(Thing.id == other)
        choice = Null()
        choice.mypick = my.thing.title
        choice.otherpick = other.thing.title
        choice.mypercent = str(round(100*my.wins/(my.matchups or 1), 2))+'%'
        choice.otherpercent = str(round(100*other.wins/(other.matchups or 1), 2))+'%'
    else:
        choice = None
    left = choose_thing()
    right = choose_thing([left])
    return render_template('index.html', left=left, right=right, choice=choice)
