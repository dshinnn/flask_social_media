from app import app
from flask import render_template, redirect, url_for, flash
from app.models import User
from app.forms import RegisterForm

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