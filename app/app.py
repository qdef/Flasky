from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from scraping import Scraping
from forms import PostSearchForm
import sqlite3

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

@app.route('/', methods=['GET', 'POST'])
def home():
	posts = BlogPost.query.all()[:10]
	search = PostSearchForm(request.form)
	if request.method == 'POST':
		return search_results(search)
	return render_template('home.html', posts=posts, form=search)

@app.route('/search')
def search_results(search):
	results = []
	search_string = search.data['search']
	posts = BlogPost.query.all()
	#if not results:
		#flash('Sorry, no results matched your post search.')
		#return redirect(url_for('blog'))
	return render_template('search.html', search_string=search_string, posts=posts, form=search)


@app.route('/blog', methods=['GET', 'POST'])
def blog():
	search = PostSearchForm(request.form)
	if request.method == 'POST':
		return search_results(search)
	posts = BlogPost.query.all()
	return render_template('blog.html', posts=posts, form=search)

#Post management routes

@app.route('/create', methods=['GET', 'POST'])
def create():
	search = PostSearchForm(request.form)
	if request.method == 'POST':
		return search_results(search)	
	return render_template('create.html', form=search)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def blogpost(post_id):
	search = PostSearchForm(request.form)
	if request.method == 'POST':
		return search_results(search)	
	post = BlogPost.query.filter_by(post_id=post_id).one()
	return render_template('detail.html', post=post, form=search)


@app.route('/addpost', methods=['GET', 'POST'])
def addpost():
	search = PostSearchForm(request.form)
	if request.method == 'POST':
		return search_results(search)	
	try:
		title = request.form['title']
		author = request.form['author']
		content = request.form['content']
		post = BlogPost(title=title, author=author, content=content, created=datetime.now(), updated=datetime.now())
		db.session.add(post)
		db.session.commit() #Adding the post to the database.
		flash('Your post was successfully created!')
		return redirect(url_for('blog'), form=search)
	except:
		flash('Your post was not created successfully. Please try again.')	
		return redirect(url_for('blog'), form=search)

@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
	search = PostSearchForm(request.form)
	if request.method == 'POST':
		return search_results(search)	
	try:
		post = BlogPost.query.filter_by(post_id=post_id).one()
		db.session.delete(post)
		db.session.commit()
		flash('The post has been successfully deleted.')
		return redirect(url_for('blog'))
	except:
		flash('The deletion process was unsuccessful.')
		return redirect(url_for('blog'), form=search)


# Other pages routes

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	search = PostSearchForm(request.form)
	if request.method == 'POST':
		return search_results(search)	
	return render_template('contact.html', form=search)

@app.route('/about', methods=['GET', 'POST'])
def about():
	search = PostSearchForm(request.form)
	if request.method == 'POST':
		return search_results(search)	
	return render_template('about.html', form=search)

@app.route('/data', methods=['GET', 'POST'])
def data():
	search = PostSearchForm(request.form)
	if request.method == 'POST':
		return search_results(search)	
	all_temperatures = Scraping()
	longyearbyen=all_temperatures.Longyearbyen()
	yellowknife=all_temperatures.Yellowknife()
	iqaluit=all_temperatures.Iqaluit()
	nuuk=all_temperatures.Nuuk()
	qaanaaq=all_temperatures.Qaanaaq()
	khatanga=all_temperatures.Khatanga()
	return render_template('data.html', longyearbyen=longyearbyen, yellowknife=yellowknife, iqaluit=iqaluit, nuuk=nuuk, qaanaaq=qaanaaq, khatanga=khatanga, form=search)

@app.context_processor
def inject_now():
	return {'now': datetime.utcnow()}

if __name__ == '__main__':
	app.run(debug=True)