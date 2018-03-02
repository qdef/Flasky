from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])	
	
class RegisterForm(FlaskForm):
	email = StringField('e-mail', validators = [InputRequired(), Email(message='Invalid e-mail'), Length(max=70)])
	username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])

#User database
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	public_id = db.Column(db.String(50), unique=True)
	username = db.Column(db.String(20), unique=True)
	password=db.Column(db.String(80))
	email = db.Column(db.String(70), unique=True)
	admin = db.Column(db.Boolean)
	
#Blog posts database
class BlogPost(db.Model):
	post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(150))
	image = db.Column(db.LargeBinary)
	image2 = db.Column(db.LargeBinary)
	author = db.Column(db.String(20))
	created = db.Column(db.DateTime)
	updated = db.Column(db.DateTime)
	content = db.Column(db.Text)
	
#Marshmallow classes: 
class UserSchema(ma.ModelSchema):
	class Meta:
		model = User

class PostSchema(ma.ModelSchema):
	class Meta:
		model = BlogPost	