from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Post, Comment
from app.forms import RegisterForm, LoginForm

@app.route('/')
def index():
    return render_template('index.html')

# Register new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user_exist = User.query.filter((User.username==username) | (User.email==email))

        if not user_exist:
            User(username=username, email=email, password=password)
            flash('Username has been successfully created!', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'{username} or {email} already exists, please login or register with a different username.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)

# Log user in
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash(f'Incorrect username/password or {user.username} does not exist', 'warning')
            return redirect(url_for('login'))
        else:
            login_user(user)
            flash('You have successfully logged in', 'success')
            return redirect(url_for('index'))

    return render_template('login.html', form=form)

# Log user out
@app.route('/logout')
def logout():
    logout_user()
    flash('You have succcessfully logged out', 'success')
    return redirect(url_for('index'))