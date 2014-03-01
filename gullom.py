# GULLOM
# Gif Ultra-Light Library Online Manager
# Hacked really (too) quickly by Raveline
# (Yeah, the title is bad. Sue me.)

from flask import Flask, g, request, session, redirect, url_for, abort, render_template, jsonify
from contextlib import closing
import sqlite3
import config

# App generation
app = Flask(__name__)
app.config.from_object(config)

### PAGES ###

# Basic
@app.route('/')
def pick():
    tags = tags()
    gifs = gifs()
    return render_template('pick.html', 
            tags = tags, 
            gifs = gifs)

# Single dream page
@app.route('/add/')
def add_menu(dream_id):
    pass

### JSON "SERVICES" ###

# Add a dream
@app.route('/add', methods=['POST'])
def add_gif(self):
    if not session.get('logged_in'):
        abort(403)

@app.route('/add', methods=['GET'])
def discriminate():
    # Get selected tags
    tags = []
    # Return available gifs
    gifs = gifs(tags)
    return jsonify(gifs)

# Login
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('admin'))
    # Check if user is connected
    login = request.form['login']
    password = request.form['password']
    if login != app.config['USERNAME'] and password != app.config['PASSWORD']:
        return render_template('login.html', error="Wrong login or password.")
    else:
        session['logged_in'] = True
        return redirect(url_for('admin'))

# Logout
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('main_page'))

### INTERCEPTORS ###

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception=None):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# DB shortcuts

def gif2dict(res):
    return [dict(name=row[0], path=row[1]) for row in res]

def tag2dict(res):
    return [dict(tagid=row[0], name=row[1]) for row in res]

def get_gifs_with_tags(tags):
    cur = g.db.execute("""select gif_name, gif_file from gifs 
            LEFT JOIN
                gifs_to_tags 
            ON
                gif_id = gtt_gif
            WHERE gtt_tag IN (?);""", [tags])
    return gif2dict(cur.fetchall())

def get_gifs():
    cur = g.db.execute('select gif_name, gif_file from gifs;')
    return gif2dict(cur.fetchall())


def get_tags():
    cur = g.db.execute('select * from tags')
    return tag2dict(cur.fetchall())

def delete_gif(gif_id):
    g.db.execute('delete from gifs where gif_id = ?', [gif_id])
    g.db.commit()

def delete_tag(tag_id):
    g.db.execute('delete from tags where tag_id = ?', [tag_id])
    g.db.commit()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


# DB init method for deployment
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

if __name__ == '__main__':
    app.run()
