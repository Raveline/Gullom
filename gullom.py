# GULLOM
# Gif Ultra-Light Library Online Manager
# Hacked really (too) quickly by Raveline
# (Yeah, the title is bad. Sue me.)

from flask import Flask, g, request, session, redirect, url_for, abort, render_template, jsonify
from contextlib import closing
import sqlite3
import config
import sys
import logging
from functools import wraps

import downloader
import meme_generator as memegen

# App generation
app = Flask(__name__)
app.config.from_object(config)


### DECORATORS ###

def login_required(f):
    """Make sure the user is logged in. If not, redirct him to the login page."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login_page', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

### PAGES ###

# Basic
@app.route('/')
@login_required
def pick():
    """Present the basic interface for picking gifs. Will display most recently
    added gifs."""
    return render_template('pick.html', 
            tags = tags(), 
            gifs = gifs())

# Add menu
@app.route('/add')
@login_required
def add():
    """Display the interface for adding new gifs."""
    return render_template('add.html',
            tags = tags())

@app.route('/stats')
@login_required
def stats():
    """Get basic stats about this installation of Gullom"""
    return render_template('stats.html',
            gif_number = count_gifs(),
            gif_size = downloader.size_of_folder(app.config['ROOT']))

### JSON "SERVICES" ###

@app.route('/gif', methods=['POST'])
@login_required
def add_gif():
    """Add the gif. Get url, name and tags from the form. Get a counter from the database.
    The counter is implemented as a separate value, not a count from the gif table, to prevent
    collisions, though very theoretically, simultaneous connexion could still collide.
    The gif will be donwloaded and only then added to the database."""
    url = request.form['url']
    name = request.form['name']
    tags = request.form['tags']
    try:
        increment_gif_number()
        filename = downloader.download(app.config['ROOT'] + "static/img/", url,get_gifs_number())
        tags = tags.split(",")
        add_new_gif(filename, name, tags)
        return jsonify({'result':'success'})
    except IOError, e:
        return jsonify({'result':'Error : could not write file on server.', 'cause':str(e)})

@app.route('/gifs/', methods=['GET'])
@login_required
def discriminate():
    """Select gifs having a list of given tags. Tags should be passed as an array."""
    # Get selected tags and convert them to 
    # int (and, in doing so, make sure we have proper input
    try:
        tags = convert_tags(request.args.getlist('tags[]'))
        # get gifs
        result = gifs(tags)
        # Return available gifs
        if result:
            return jsonify({'result':'success', 'gifs': result})
        else:
            return jsonify({'result':'empty'})
    except ValueError:
        return jsonify({'result':'Error - invalid input.'})

@app.route('/memeadd', methods=["GET"])
@login_required
def add_meme():
    """Meme addition form"""
    return render_template('memeadd.html')

@app.route('/memeadd', methods=["POST"])
@login_required
def post_meme():
    """Add the meme to the database, with the same workflow as add_gif."""
    url = request.form['url']
    name = request.form['name']
    text1 = request.form['text1']
    text2 = request.form['text2']
    try:
        increment_meme_number()
        filename = downloader.download(app.config['ROOT'] + "static/storedmemes/", url,get_memes_number())
        add_new_meme(filename, name, text1, text2)
        return jsonify({'result':'success'})
    except IOError, e:
        return jsonify({'result':'Error : could not write file on server.', 'case':str(e)})

@app.route('/memecreate', methods=["GET"])
@login_required
def create_meme():
    """Access to the meme creation form."""
    return render_template("memecreate.html", memes = get_memes())

@app.route('/memepost', methods=["POST"])
def render_meme():
    """Return for a meme creation."""
    text1 = request.form['text1'].upper()
    text2 = request.form['text2'].upper()
    template = request.form['filename']
    mg = memegen.MemeGenerator(app.config['ROOT'] + "static/storedmemes/" + template)
    increment_memegen_number()
    mg.add_text(text1, text2, app.config['ROOT'] + "static/meme/", get_memegen_number()) 
    return jsonify({'result':'success', 'file': "static/meme/" + mg.get_file_name()})

@app.route('/tag', methods=['POST'])
@login_required
def add_tag():
    """Add a tag to the database."""
    tag_id = add_new_tag(request.form['tag'])
    #except Exception:
    #    return jsonify({'result':'error'})
    return jsonify({'result':'success', 'id':tag_id})

@app.route('/tag/<tagid>', methods=['DELETE'])
@login_required
def remove_tag(tagid):
    """Remove a tag from the database."""
    delete_tag(tagid)
    return jsonify({'result':'success'})

# Login
@app.route('/login', methods=['GET'])
def login_page():
    """Display the login interface."""
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """Log the user if necessary."""
    if session.get('logged_in'):
        return redirect(url_for('pick'))
    # Check if user is connected
    login = request.form['login']
    password = request.form['password']
    if login != app.config['USERNAME'] or password != app.config['PASSWORD']:
        return render_template('login.html', error="Wrong login or password.")
    else:
        session['logged_in'] = True
        return redirect(url_for('pick'))

# Logout
@app.route('/logout')
@login_required
def logout():
    """Log-out the user."""
    session['logged_in'] = False
    return render_template('login.html')

### INTERCEPTORS ###

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception=None):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# Accessors
def tags():
    return get_tags()

def gifs (filt = None):
    if filt is None or not filt:
        return get_gifs()
    else:
        return get_gifs_with_tags(filt)

def convert_tags(tags):
    return map(int, tags)

# DB shortcuts

def add_new_gif(filename, name, tags):
    last_id = insert_gif(filename, name)
    insert_tags (last_id, tags)

def add_new_meme(filename, name, text1, text2):
    insert_meme(filename, name, text1, text2)

def add_new_tag(tag):
    cur = g.db.execute("insert into tags values (NULL, ?)", [tag])
    g.db.commit()
    return cur.lastrowid

def insert_tags(last_id, tags):
    for tag in tags:
        g.db.execute("insert into gifs_to_tags values (NULL, ?, ?);",
                [last_id, tag])
        g.db.commit()

def insert_gif(filename, name):
    cur = g.db.execute("insert into gifs values (NULL, ?, ?);",
            [name, filename])
    g.db.commit()
    return cur.lastrowid

def insert_meme(filename, name, text1, text2):
    cur = g.db.execute("insert into memes values (NULL, ?, ?, ?, ?);",
            [filename, name, text1, text2])
    g.db.commit()
    return cur.lastrowid

def gif2dict(res):
    if not res or res[0][0] is None:
        return [] 
    return [dict(tags=stringify_tags(row[0]), name=row[1], path="static/img/"+row[2]) for row in res]

def stringify_tags(tags):
    if tags is None:
        return ""
    else:
        return tags.split('@@@')

def tag2dict(res):
    return [dict(tagid=row[0], name=row[1]) for row in res]

def meme2dict(res):
    return [dict(mfile=row[0], name=row[1], text1=row[2], text2=row[3]) for row in res]

def get_gifs_with_tags(tags):
    cur = g.db.execute("""select group_concat(tag_name, '@@@'), gif_name, gif_file from gifs 
            LEFT JOIN
                gifs_to_tags 
            ON
                gif_id = gtt_gif
            LEFT JOIN
                tags
            ON
                gtt_tag = tag_id
            WHERE {seq}
            GROUP BY gif_name;""".format(seq=' AND '.join(['gtt_tag = ?']*len(tags))), tags)
    return gif2dict(cur.fetchall())

def get_gifs():
    cur = g.db.execute("""select group_concat(tag_name, '@@@'), gif_name, gif_file from gifs
                        LEFT JOIN
                            gifs_to_tags
                        ON
                            gtt_gif = gif_id
                        LEFT JOIN
                            tags
                        ON
                            tag_id = gtt_tag
                        GROUP BY gif_name;""")
    return gif2dict(cur.fetchall())

def count_gifs():
    cur = g.db.execute('select count(*) from gifs')
    return cur.fetchall()[0][0]

def get_gifs_number():
    return get_param("gifcount")

def get_memes_number():
    return get_param("memecount")

def get_memegen_number():
    return get_param("memegencount")

def get_param(name):
    cur = g.db.execute('select (param_val) from params where param_key = ?', [name])
    return cur.fetchall()[0][0]

def increment_param(name):
    cur = g.db.execute('update params set param_val = param_val + 1 where param_key = ?', [name])
    g.db.commit()

def increment_gif_number():
    increment_param("gifcount")

def increment_meme_number():
    increment_param("memecount")

def increment_memegen_number():
    increment_param("memegencount")

def get_tags():
    cur = g.db.execute('select * from tags order by tag_name')
    return tag2dict(cur.fetchall())

def get_memes():
    cur = g.db.execute('select meme_file, meme_name, meme_txt1, meme_txt2 from memes order by meme_name');
    return meme2dict(cur.fetchall())

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

