from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.role}')"
        

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(10), nullable=False)
    course_name = db.Column(db.String(100), nullable=True)
    
    def __repr__(self):
        return f"Course('{self.id}', '{self.course_code}', '{self.course_name}')"


class Faculty(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Faculty('{self.id}', '{self.username}', '{self.email}', '{self.role}')"


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    facad = db.Column(db.String(30), nullable=True)
    role = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Course('{self.id}', '{self.username}', '{self.email}', '{self.roll_number}', '{self.phone_number}', '{self.facad}' '{self.role}')"
