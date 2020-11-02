from database import *
from flask import Flask, request, render_template
import random

app = Flask(__name__)

def choose_thing(*exclude):
    thing = None
    max_id = Thing.select(fn.Max(Thing.id)).scalar()
    while thing in exclude or thing is None:
        thing = Thing.select().where(Thing.id >= random.randint(0, max_id)).get()
    return thing

class Null:
    pass

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        my = int(request.form['my-choice-id'])
        other = int(request.form['other-id'])
        Thing.update(matchups = Thing.matchups+1).where(Thing.id.in_([my, other])).execute()
        Thing.update(wins = Thing.wins + 1).where(Thing.id == my).execute()
        my = Thing.get(Thing.id == my)
        other = Thing.get(Thing.id == other)
        choice = Null()
        choice.mypick = my.title
        choice.otherpick = other.title
        choice.mypercent = str(round(100*my.wins/(my.matchups or 1), 2))+'%'
        choice.otherpercent = str(round(100*other.wins/(other.matchups or 1), 2))+'%'
        choice.agree = my.wins/(my.matchups or 1) > other.wins/(other.matchups or 1)
        print(my.title, 'over', other.title, '(', choice.mypercent, 'over', choice.otherpercent, ')')
    else:
        choice = None
    left = choose_thing()
    right = choose_thing(left)
    return render_template('index.html', left=left, right=right, choice=choice)

@app.route('/rankings')
def rankings():
    bottom = Thing.select().order_by((Thing.wins/Thing.matchups), Thing.wins, Thing.matchups).limit(20)
    top = Thing.select().order_by(-(Thing.wins/Thing.matchups), -Thing.wins, -Thing.matchups).limit(20)

    return render_template('rankings.html', top_query=top, bot_query=bottom)

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
