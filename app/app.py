from flask import Flask, flash, render_template, request, session, redirect, url_for, jsonify, make_response, Response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime, timedelta
from weather_api import WeatherAPI
from flask_marshmallow import Marshmallow
from forms import LoginForm, RegisterForm, User, BlogPost, UserSchema, PostSchema
from functools import wraps
import uuid

#Flask app initiation and configuration:
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Database creation:
db = SQLAlchemy(app)
ma = Marshmallow(app)

#Login system initiation:
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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

#This function extracts data from an API display real-time temperatures.
@app.route('/data', methods=['GET'])
def data():
	temperatures = WeatherAPI()
	northpole = temperatures.api_call(90.0, 0.0)
	longyearbyen = temperatures.api_call(78.21, 15.54)
	alert = temperatures.api_call(82.50, -62.34)
	iqaluit = temperatures.api_call(63.74, -68.51)
	northgreenland = temperatures.api_call(83.63, -34.04)
	qaanaaq = temperatures.api_call(77.46, -69.22)
	nordvik = temperatures.api_call(74.01, 111.47)
	rudolf = temperatures.api_call(81.78, 58.66)
	return render_template('data.html', northpole=northpole, alert=alert, iqaluit=iqaluit, northgreenland=northgreenland, qaanaaq=qaanaaq, nordvik=nordvik, rudolf=rudolf, longyearbyen=longyearbyen)


#__________________________USERS MANAGEMENT_____________________________

#Loading an existing user from the database
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

#Function to sign up to the website
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = RegisterForm()
	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data, method='sha256')
		new_user=User(public_id=str(uuid.uuid4()), username=form.username.data, email=form.email.data, password=hashed_password, admin=False)
		db.session.add(new_user)
		db.session.commit()
		flash('New user has been successfully created! Please enter your credentials to login.')
		return redirect(url_for('login'))
	else:
		flash('Username has to be less than 50 characters. Password must be between 6 and 80 characters.')
		return render_template('signup.html', form=form)

#Function to login
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
	flash('Failed to log in. Please verify your username and password and try again.')
	return render_template('login.html', form=form)

#Function to logout
@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You successfully logged out.')
	return redirect(url_for('blog'))

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

# Function to edit a post (only for its author)
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

# Function to delete a post (only for its author)
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

@app.route('/api', methods=['GET'])
def api():
	return render_template('api.html')

#Displays all posts of the blog in JSON format (serialized with Marshmallow)
@app.route('/api/posts')
def get_all_posts():
	posts = BlogPost.query.all()
	posts_schema = PostSchema(many=True)
	output = posts_schema.dump(posts).data
	return jsonify({'posts': output})

#Form to pick the post id that has to be extracted in JSON format
@app.route('/api/post-id', methods=['GET'])
@login_required
def detail_post_id():
	return render_template('api-detail-post.html')

#Displays one specific blog post in JSON format.
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
	posts_schema = PostSchema()
	output = posts_schema.dump(post).data
	return jsonify({'post': output})


#Displays all users of the blog in JSON format (if the current user is admin)
@app.route('/api/users', methods=['GET'])
@login_required
def get_all_users():
	if current_user.admin :
		users = User.query.all()
		users_schema = UserSchema(many=True)
		output = users_schema.dump(users).data
		return jsonify({'users': output})
	flash('Only admins can access the users list.')
	return redirect(url_for('api'))

#Displays the information on the current user in JSON format.
@app.route('/api/user-info', methods=['GET'])
@login_required
def get_one_user():
	user = User.query.filter_by(username=current_user.username).first()
	user_schema = UserSchema()
	output = user_schema.dump(user).data
	return jsonify({'user': output})

#__________________________________________________________________

#This function is necessary to display the current time with Jinja2:
@app.context_processor
def inject_now():
	return {'now': datetime.utcnow()}


if __name__ == '__main__':
	app.run(debug=True)
	db.create_all()