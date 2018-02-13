from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from scraping import Scraping

# The static url path is essential to render the bootstrap correctly.
app = Flask(__name__)
app.secret_key = "super secret key"

#_______________POST DATABASE_______________

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

#_______________ROUTES_______________

@app.route('/')
def home():
	posts = BlogPost.query.all()[:10]
	return render_template('home.html', posts=posts)

@app.route('/blog')
def blog():
	posts = BlogPost.query.all()
	return render_template('blog.html', posts=posts)

#Post management routes

@app.route('/create')
def create():
	return render_template('create.html')

@app.route('/post/<int:post_id>')
def blogpost(post_id):
	post = BlogPost.query.filter_by(post_id=post_id).one()
	return render_template('detail.html', post=post)

@app.route('/addpost', methods=['POST'])
def addpost():
	title = request.form['title']
	author = request.form['author']
	content = request.form['content']
	post = BlogPost(title=title, author=author, content=content, created=datetime.now(), updated=datetime.now())
	db.session.add(post)
	db.session.commit() #Adding the post to the database.
	return redirect(url_for('blog'))

@app.route('/delete/<int:post_id>', methods=['GET'])
def delete(post_id):
	try:
		post = BlogPost.query.filter_by(post_id=post_id).one()
		db.session.delete(post)
		db.session.commit()
		flash('The post has been successfully deleted.')
		return redirect(url_for('blog'))
	except:
		return flash('The deletion process was unsuccessful.')


# Other pages routes

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/data')
def data():
	all_temperatures = Scraping()
	longyearbyen=all_temperatures.Longyearbyen()
	yellowknife=all_temperatures.Yellowknife()
	iqaluit=all_temperatures.Iqaluit()
	nuuk=all_temperatures.Nuuk()
	qaanaaq=all_temperatures.Qaanaaq()
	khatanga=all_temperatures.Khatanga()
	return render_template('data.html', longyearbyen=longyearbyen, yellowknife=yellowknife, iqaluit=iqaluit, nuuk=nuuk, qaanaaq=qaanaaq, khatanga=khatanga)

@app.context_processor
def inject_now():
	return {'now': datetime.utcnow()}

if __name__ == '__main__':
	app.run(debug=True)