from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

import datetime

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.secret_key='bittiger'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(600))
    timestamp = db.Column(db.Datetime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

db.create_all()
db.session.commit()

user = User(username='unclebarney')
db.session.add()
db.session.commit()

"""
index
    - find all the blog posts
    - go to signup
    - if already login find all the blog posts
    - if already login, go to create blog page

signup
    - create new user account
    - after create, redirect to index

login
    - a form to login
    - after login, redirect to index

logout (no html page)
    -logout user

create
    - a form to create blog
    - after creation, redirect to index
"""
@app.route('/')
def index():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        if not user:
            session.pop('username', None)
            return render_template('index.html')
        blogs = user.posts.all()
        return render_template('index.html', user=user, blogs=blogs)
    return render_template('index.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        session['username']=username
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        content = request.form['content']
        user = User.query.filter_by(username=session['username'])
        post = Post(content=content, timestamp=datetime.datetime.utc(), author = user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.error_handler(404)
def page_not_found(error):
    return render_template('404.html'), 404

app.run(debug=True)