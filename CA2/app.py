from flask import Flask, render_template, redirect, request, session, g, url_for
from database import get_db, close_db
from flask_session import Session
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'MYKEY'
Session(app)
app.teardown_appcontext(close_db)

@app.before_request
def load_gamer():
    g.gamer = session.get('gamer', None)



def log_check(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.gamer is None:
            return redirect(url_for('ask_name', next = request.url))
        return view(*args, **kwargs)
    return wrapped_view

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gamer_assign', methods=['GET','POST'])
def ask_name():
    form = GamerForm()
    if form.validate_on_submit():
        session['gamer'] = form.gamer.data
        session.modified = True
        g.gamer = session['gamer']
        next_page = request.args.get('next')
        return redirect(next_page)
    return render_template('gamerAssign.html', form = form)





@app.route('/introduction')
def introduction():
    return render_template('introduction.html')

@app.route('/quote')
def quote():
    return render_template('quote.html')

@app.route('/leaderboard')
def leaderboard():
    db = get_db()
    leaders = db.execute('''
        SELECT * FROM leaderBoard
        ORDER BY reached_floor DESC
        LIMIT 10''').fetchall()

    return render_template('leaderboard.html', leaders = leaders)


@app.route('/choose_character')
@log_check
def choose():
    return render_template('choose.html')

@app.route('/game')
@log_check
def game():
    if 'data' not in session:
        return redirect(url_for('choose'))
    data = session['data']
    session.pop('data')
    return render_template('game.html', data = data)

@app.route('/record', methods=['POST'])
def record():
    record = int(request.form['score'])
    character = request.form['character']
    name = g.gamer
    db = get_db()
    db.execute('''
        INSERT INTO leaderBoard VALUES(?,?,?)
        ''',(name, character, record))
    db.commit()
    return 'y'

@app.route('/knight')
@log_check
def knight():
    session['data'] = {
            'role': 'knight',
            'HP': 12,
            'weapon': 'sword',
            'speed': 4,
            'skill': 'slashing',
            'AP': 5,
            'ACD': 0.5,
            'SAP': 7,
            'SCD': 5,
            'skillPre':750 ,
            'attackPre': 200,
            'skillDuration':150,
            'attackDuration':150,
            'HUpTimes':1,
            'HWithLvUp':2,
            'AUpTimes':5,
            'AWithLvUp':2
            }
    return redirect('game')

@app.route('/warrior')
@log_check
def warrior():
    session['data'] = {
            'role': 'warrior',
            'HP': 20,
            'weapon': 'shield',
            'speed': 2.5,
            'skill': 'rushing',
            'AP': 3,
            'ACD': 0.5,
            'SAP': 20,
            'SCD': 10,
            'skillPre':1000,
            'attackPre': 200,
            'skillDuration':300,
            'attackDuration':150,
            'HUpTimes':1,
            'HWithLvUp':5,
            'AUpTimes':5,
            'AWithLvUp':1
            }
    return redirect('game')

@app.route('/mage')
@log_check
def mage():
    session['data'] = {
            'role': 'mage',
            'HP': 8,
            'weapon': 'staff',
            'speed': 3,
            'skill': 'burst',
            'AP': 3,
            'ACD': 1.5,
            'SAP': 6,
            'SCD': 20,
            'skillPre':1000,
            'attackPre': 200,
            'skillDuration':5000,
            'attackDuration':200,
            'HUpTimes':4,
            'HWithLvUp':1,
            'AUpTimes':3,
            'AWithLvUp':1
            }
    return redirect('game')

@app.route('/priest')
@log_check
def priest():
    session['data'] = {
            'role': 'priest',
            'HP': 6,
            'weapon': 'scripture',
            'speed': 3,
            'skill': 'meteorite',
            'AP': 8,
            'ACD': 2,
            'SAP': 2,
            'SCD': 2
            }
    return redirect('game')


@app.route('/assassin')
@log_check
def assassin():
    session['data'] = {
            'role': 'assassin',
            'HP': 8,
            'weapon': 'dagger',
            'speed': 5,
            'skill': 'assassinating',
            'AP': 4,
            'ACD': 0.5,
            'SAP': 15,
            'SCD': 15

            }
    return redirect('game')

@app.route('/hunter')
@log_check
def hunter():
    session['data'] = {
            'role': 'hunter',
            'HP': 10,
            'weapon': 'shotgun',
            'speed': 4,
            'skill': 'scatter',
            'AP': 15,
            'ACD': 3,
            'SAP': 15,
            'SCD': 20
            }
    return redirect('game')

class GamerForm(FlaskForm):
    gamer = StringField('Nickname:',
                            validators=[InputRequired()])
    submit = SubmitField('OK')