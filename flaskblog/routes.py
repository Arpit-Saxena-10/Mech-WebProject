from flask import render_template, url_for, flash, redirect, request
from flaskblog.models import User, Course
from flaskblog.forms import LoginForm, AllotmentForm
from flaskblog import app, db , bcrypt
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    courses = Course.query.all()
    return render_template('home.html', courses=courses)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if user and bcrypt.check_password_hash(user.password, form.password.data):
        if user and form.password.data == user.password:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route("/course/<int:course_id>")
def course(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course.html', title=course.course_code, course=course)


@app.route("/allotment", methods=['GET', 'POST'])
@login_required
def allotment():
    form = AllotmentForm()
    if form.validate_on_submit():
        db.session.commit()
        flash('Student Has been Succesfully Alloted!', 'success')
        return redirect(url_for('home'))
    
    return render_template('allotment.html', title='Allotment', form=form,)
