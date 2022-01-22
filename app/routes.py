from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Post, Comment
from app.forms import RegisterForm, LoginForm, PostForm, CommentForm

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

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

# Creates a new post
@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        post_section = form.post_section.data
        user_id = current_user.id

        Post(title=title, post_section=post_section, user_id=user_id)
        flash('Your post has been created', 'success')
        return redirect(url_for('index', form=form))
    
    return render_template('create_post.html', form=form)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_info(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = form.comment.data
        user_id = current_user.id
        post_id = post.id
        Comment(comment_section=comment, user_id=user_id, post_id=post_id)
        flash('Comment has been posted', 'secondary')
        return redirect(url_for('post_info', post_id=post.id))

    return render_template('post.html', post=post, form=form)

@app.route('/post/<int:post_id>/edit_post', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if current_user.id != post.user_id:
        flash("Error: Cannot edit someone else's post", "danger")
        return redirect(url_for('post_info', post_id=post.id))
    
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.post_section = form.post_section.data

        post.save_post()
        flash('Post has been updated', 'primary')
        return redirect(url_for('post_info', post_id=post.id))
    return render_template('edit_post.html', post=post, form=form)

@app.route('/post/<int:post_id>/delete_post', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id != post.user_id:
        flash("You cannot delete someone else's post", "danger")
        return redirect(url_for('post_info'), post_id=post.id)
    post.delete_post()
    flash('Post has been deleted', 'success')
    return redirect(url_for('index'))