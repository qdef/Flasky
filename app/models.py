from flask_sqlalchemy import SQLAlchemy
from flask import Flask

#_______________POST  DATABASE_______________

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)

class BlogPost(db.Model):
	post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(150))
	image = db.Column(db.LargeBinary)
	image2 = db.Column(db.LargeBinary)
	author = db.Column(db.String(20))
	created = db.Column(db.DateTime)
	updated = db.Column(db.DateTime)
	content = db.Column(db.Text)