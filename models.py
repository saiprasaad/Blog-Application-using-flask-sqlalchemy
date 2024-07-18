from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    posts = db.relationship('Post', backref = 'user', lazy = False)
    comments = db.relationship('Comment', backref = 'user', lazy = False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    comments = db.relationship('Comment', backref='post', lazy = False)

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(1000))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __init__(self, content, post_id, user_id):
        self.content = content
        self.post_id = post_id
        self.user_id = user_id