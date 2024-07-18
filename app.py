from flask import Flask, jsonify
from blog_bp import blog_bp
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Secret@123'
app.register_blueprint(blog_bp)
db.init_app(app)

@app.errorhandler(500)
@app.errorhandler(403)
@app.errorhandler(404)
def handle_error(error):
     return jsonify({'error':f'{error}'}), error.code

if __name__ == '__main__':
    # used to know which applicaton instance to use while creating db
    with app.app_context():
        db.create_all()

    app.run(debug=True) 