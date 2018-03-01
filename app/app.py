from flask import Flask, flash, render_template, request, session, redirect, url_for, jsonify, make_response, Response
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from datetime import date, datetime, timedelta
from scraping import Scraping
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from functools import wraps
import uuid
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#_____________________DATABASES_____________________

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
	
class RegisterForm(FlaskForm):
	email = StringField('e-mail', validators = [InputRequired(), Email(message='Invalid e-mail'), Length(max=70)])
	username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	public_id = db.Column(db.String(50), unique=True)
	username = db.Column(db.String(20), unique=True)
	password=db.Column(db.String(80))
	email = db.Column(db.String(70), unique=True)
	admin = db.Column(db.Boolean)
	
class BlogPost(db.Model):
	post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(150))
	image = db.Column(db.LargeBinary)
	image2 = db.Column(db.LargeBinary)
	author = db.Column(db.String(20))
	created = db.Column(db.DateTime)
	updated = db.Column(db.DateTime)
	content = db.Column(db.Text)
	

#__________________________USERS MANAGEMENT_____________________________

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = RegisterForm()
	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data, method='sha256')
		hashed_password
		new_user=User(public_id=str(uuid.uuid4()), username=form.username.data, email=form.email.data, password=hashed_password, admin=False)
		db.session.add(new_user)
		db.session.commit()
		flash('New user has been successfully created!')
		return redirect(url_for('blog'))
	else:
		flash('Username has to be less than 50 characters. Password must be between 6 and 80 characters.')
		return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user= User.query.filter_by(username=form.username.data).first()
		if user:
			if check_password_hash(user.password, form.password.data):
				login_user(user, remember=True)
				flash('You successfully logged in.')
				return redirect(url_for('blog'))
	#flash('Failed to log in. Please verify your username and password and try again.')
	return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You successfully logged out.')
	return redirect(url_for('blog'))

#__________________________MAIN PAGES ROUTES_____________________________

#Function that displays the Home page:
@app.route('/', methods=['GET'])
def home():
	posts = BlogPost.query.all()[:10]
	return render_template('home.html', posts=posts)

# Function to display all the posts of the blog:
@app.route('/blog', methods=['GET'])
def blog():
	posts = BlogPost.query.all()
	return render_template('blog.html', posts=posts)

# Function to display one specific blog post:
@app.route('/post/<int:post_id>', methods=['GET'])
def blogpost(post_id):
	post = BlogPost.query.filter_by(post_id=post_id).first()
	return render_template('detail.html', post=post)

#This function displays the 'Contact' page.
@app.route('/contact', methods=['GET'])
def contact():
	return render_template('contact.html')

#This function displays the 'About' page.
@app.route('/about', methods=['GET'])
def about():
	return render_template('about.html')

#This function uses web scraping to display real-time temperatures.
@app.route('/data', methods=['GET'])
def data():
	all_temperatures = Scraping()
	longyearbyen =all_temperatures.Longyearbyen()
	yellowknife = all_temperatures.Yellowknife()
	iqaluit = all_temperatures.Iqaluit()
	nuuk = all_temperatures.Nuuk()
	qaanaaq = all_temperatures.Qaanaaq()
	khatanga = all_temperatures.Khatanga()
	return render_template('data.html', longyearbyen=longyearbyen, yellowknife=yellowknife, iqaluit=iqaluit, nuuk=nuuk, qaanaaq=qaanaaq, khatanga=khatanga)

@app.route('/api', methods=['GET'])
def api():
	return render_template('api.html')

#__________________________POST MANAGEMENT VIA WEBSITE_____________________________

# Function to display the post creation form:
@app.route('/create', methods=['GET'])
def create_post():
	return render_template('create_post.html')

# Function to create a new post in the database from the post creation form:
@app.route('/addpost', methods=['GET', 'POST'])
@login_required
def addpost():
	try:
		title = request.form['title']
		content = request.form['content']
		post = BlogPost(title=title, author=current_user.username, content=content, created=datetime.now(), updated=datetime.now())
		db.session.add(post)
		db.session.commit() #Adding the post to the database.
		flash('Your post was successfully created!')
		return render_template('detail.html', post=post)
	except:
		flash('Your post was not created successfully. Please try again.')	
		return redirect(url_for('blog'))

# Function to edit a post:
@app.route('/edit/post/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
	post = BlogPost.query.filter_by(post_id=post_id).first()
	if post.author != current_user.username:
		flash('Only the author of this post can modify it!')
		return redirect(url_for('blogpost', post_id=post_id))
	if request.method == 'POST':
		try:		
			title = request.form['title']
			content = request.form['content']
			post.title = title
			post.content = content
			db.session.commit()
			flash('The post was successfully edited!')
			return redirect(url_for('blog', post_id=post_id))
		except:
			flash('The post modification process failed. Please try again.')
			return redirect(url_for('blog', post_id=post_id))
	else:
		return render_template('edit.html', post=post)

# Function to delete a post:
@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
	post = BlogPost.query.filter_by(post_id=post_id).first()
	if post.author != current_user.username:
		flash('Only the author of this post can delete it!')
		return render_template('detail.html', post=post)
	try:
		db.session.delete(post)
		db.session.commit()
		flash('The post has been successfully deleted.')
		return redirect(url_for('blog'))
	except:
		flash('The deletion process was aborted. Please try again.')
		return redirect(url_for('blog'))


#__________________________DATA EXTRACTION VIA API_____________________________

@app.route('/api/posts', methods=['GET'])
@login_required
def get_all_posts():
	posts = BlogPost.query.all()
	output = []
	for post in posts:
		post_data = {}
		post_data['id'] = post.post_id
		post_data['title'] = post.title
		post_data['author'] = post.author
		post_data['created'] = post.created
		post_data['updated'] = post.updated
		post_data['content'] = post.content
		output.append(post_data)
	return jsonify({'posts': output})

@app.route('/api/post-id', methods=['GET'])
@login_required
def detail_post_id():
	return render_template('api-detail-post.html')

@app.route('/api/post-detail', methods=['POST'])
@login_required
def detail_post():
	result = request.form['number']
	try:
		result=int(result)
	except:
		return jsonify({'message': 'You must enter an integer.'})
	post = BlogPost.query.filter_by(post_id=result).first()
	if not post:
		return jsonify({'message': 'No post was found!'})
	post_data = {}
	post_data['id'] = post.post_id
	post_data['title'] = post.title
	post_data['author'] = post.author
	post_data['created'] = post.created
	post_data['updated'] = post.updated
	post_data['content'] = post.content
	return jsonify({'post': post_data})

@app.route('/api/users', methods=['GET'])
@login_required
def get_all_users():
	if current_user.admin :
		users = User.query.all()
		output = []
		for user in users:
			user_data={}
			user_data['public_id']=user.public_id
			user_data['name']=user.username
			user_data['password']=user.password
			user_data['admin']=user.admin
			user_data['email']=user.email
			output.append(user_data)
		return jsonify({'users': output})
	else:
		flash('Only admins can access the users list.')
		return redirect(url_for('api'))

@app.route('/api/user-info', methods=['GET'])
@login_required
def get_one_user():
	user = User.query.filter_by(username=current_user.username).first()
	user_data={}
	user_data['Public_id']=user.public_id
	user_data['Name']=user.username
	user_data['Password']=user.password
	user_data['Admin']=user.admin
	user_data['email']=user.email
	return jsonify({'user': user_data})

#__________________________________________________________________

#This function is necessary to display the current time with Jinja2:
@app.context_processor
def inject_now():
	return {'now': datetime.utcnow()}


if __name__ == '__main__':
	app.run(debug=True)