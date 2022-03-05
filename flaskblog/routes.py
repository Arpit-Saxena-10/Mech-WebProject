from flask import render_template, url_for, flash, redirect, request
from sqlalchemy import null
from flaskblog.models import Faculty, Student, User, Course
from flaskblog.forms import LoginForm, OTPForm
from flaskblog import app, login_manager, bcrypt
from flask_login import login_user, current_user, logout_user
from functools import wraps

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
        if user and bcrypt.check_password_hash(user.password, form.password.data):
        # if user and user.password == form.password.data :
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

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please log in to access this page.", 'info')
                return login_manager.unauthorized()
            if ((current_user.role != role) and (role != "ANY")):
                flash("You don't have the right to access this page. Redirecting to the home page", 'info')
                return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


@app.route("/account", methods=['GET'])
@login_required(role="ANY")
def account():
    if current_user.role =='admin':
        user = Faculty.query.filter_by(email=current_user.email).first()
    else:
        user = Student.query.filter_by(email=current_user.email).first()
    return render_template('account.html', title='Account', user=user)


@app.route("/course/<int:course_id>")
def course(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course.html', title=course.course_code, course=course)


@app.route("/allotment", methods=['GET', 'POST'])
@login_required(role="admin")
def allotment():
    return render_template('allotment.html', title='Allotment')


@app.route("/attendance", methods=['GET', 'POST'])
@login_required(role="student")
def attendance():
    return render_template('attendance.html', title='Attendance')


@app.route("/attendance/emailOTP", methods=['GET', 'POST'])
@login_required(role="student")
def emailOTP():
    form = OTPForm()
    return render_template('enterOTP.html', title='Verification', form=form)


@app.route("/attendance/smsOTP", methods=['GET', 'POST'])
@login_required(role="student")
def smsOTP():
    form = OTPForm()
    number = 'XXXXX12345'
    return render_template('enterOTP.html', title='Verification', form=form, number=number)


@app.route("/attendance/validateOTP", methods=['POST'])
@login_required(role="student")
def validateOTP():
    otp = request.form.get('enterOTP')
    if otp:
        flash('You have marked your attendance!', 'success')
        return redirect(url_for('attendance'))

