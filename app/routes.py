from app import app
from flask import render_template, redirect, url_for, flash
from app.models import User
from app.forms import RegisterForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        User(username=username, email=email, password=password)
        flash('Username has been successfully created!', 'success')
        return redirect(url_for('index'))
        
    return render_template('register.html', form=form)