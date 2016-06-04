from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	user = { 'nickname' : 'Miguel' }
	posts = [  # fake array of posts
		{ 
			'author': {'nickname': 'John'}, 
			'body': 'Beautiful day in Portland!' 
		},
		{ 
			'author': {'nickname': 'Susan'}, 
			'body': 'The Avengers movie was so cool!' 
		}
	]
	return render_template(
		'index.html',
		title = "Home",
		user = user,
		posts = posts,
		)

@app.route('/login', methods=['POST', 'GET'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for OpenID="%s", remember_me=%s' %
			(form.openid.data, str(form.remember_me.data)))
		return redirect('/index')
	return render_template(
		'login.html',
		title = "Login",
		form=form,
		providers=app.config['OPENID_PROVIDERS']
		)
