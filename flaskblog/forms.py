from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('login')

class AllotmentForm(FlaskForm):
    course_code = StringField('Course Code', validators=[DataRequired()])
    course_name = TextAreaField('Course Name', validators=[DataRequired()])
    submit = SubmitField('Post')

class OTPForm(FlaskForm):
    enterOTP = StringField('Enter The OTP', validators=[DataRequired()])
    submit = SubmitField('Mark Attendance')