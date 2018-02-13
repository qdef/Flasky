from wtforms import Form, StringField, SelectField

class PostSearchForm(Form):
	choices = [('title', 'title'),
               ('content', 'content'),
               ('author', 'author')]
	select = SelectField('Search for posts:', choices=choices)
	search = StringField('')