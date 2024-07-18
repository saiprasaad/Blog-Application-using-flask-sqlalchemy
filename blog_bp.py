from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for
from models import Comment, User, Post, db

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def home():
    if 'user' not in session or 'user_id' not in session:
         return redirect(url_for('blog.login'))
    posts = Post.query.all()
    return render_template('index.html', posts = posts)

@blog_bp.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if 'username' not in request.form or len(request.form['username']) == 0 or 'password' not in request.form or len(request.form['password']) == 0:
            return render_template('login.html', error = 'Missing required fields')
        
    user_info = User.query.filter_by(username=request.form['username']).first()

    if not user_info:
         return render_template('login.html', error = f"No user exists with username: {request.form['username']}")
    
    if user_info.password != request.form['password']:
         return render_template('login.html', error = 'Invalid credentials')

    session['user'] = request.form['username']
    session['user_id'] = user_info.id
    return redirect(url_for('blog.home'))

@blog_bp.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if 'username' not in request.form or len(request.form['username']) == 0 or 'password' not in request.form or len(request.form['password']) == 0:
            return render_template('register.html', error = 'Missing required fields')
        
    user_info = User(username=request.form['username'], password=request.form['password'])
    db.session.add(user_info)
    db.session.commit()
    return redirect(url_for('blog.login'))

@blog_bp.route('/logout')
def logout():
     session.pop('user', None)
     session.pop('user_id', None)
     return redirect(url_for('blog.login'))

@blog_bp.route('/create-post', methods = ['GET', 'POST'])
def create_post():
     if request.method == 'GET':
          return render_template('create-post.html')
     
     if 'user' not in session or 'user_id' not in session:
         return redirect(url_for('blog.login'))
    
     if 'title' not in request.form or len(request.form['title']) == 0 or 'content' not in request.form or len(request.form['content']) == 0:
          return render_template('create-post.html', error = 'Missing required fields')
     
     post_info = Post(title = request.form['title'], content = request.form['content'], user_id=session['user_id'])
     db.session.add(post_info)
     db.session.commit()
     return redirect(url_for('blog.home'))

@blog_bp.route('/edit-post/<id>', methods = ['GET', 'POST'])
def edit_post(id):
     post_info = Post.query.filter_by(id=id).first()

     if request.method == 'GET':
          print(post_info)
          return render_template('edit-post.html', post=post_info)
    
     if 'user' not in session or 'user_id' not in session:
         return redirect(url_for('blog.login'))
     
     if 'title' not in request.form or len(request.form['title']) == 0 or 'content' not in request.form or len(request.form['content']) == 0:
          return render_template('edit-post.html', error = 'Missing required fields')
     
     post_info.title = request.form['title']
     post_info.content = request.form['content']
     db.session.commit()

     return redirect(url_for('blog.home'))

@blog_bp.route('/delete-post/<id>', methods = ['GET'])
def delete_post(id):
     Post.query.filter_by(id=id).delete()
     db.session.commit()

     return redirect(url_for('blog.home'))

@blog_bp.route('/add-comment/<post_id>', methods = ["POST"])
def add_comment(post_id):
     if 'user' not in session or 'user_id' not in session:
         return redirect(url_for('blog.login'))
     comment_obj = Comment(content=request.form['content'], post_id=post_id, user_id=session['user_id'])
     db.session.add(comment_obj)
     db.session.commit()
     return redirect(url_for('blog.home'))

@blog_bp.route('/delete-comment/<id>')
def delete_comment(id):
     if 'user' not in session or 'user_id' not in session:
         return redirect(url_for('blog.login'))
     Comment.query.filter_by(id=id).delete()
     db.session.commit()
     return redirect(url_for('blog.home'))