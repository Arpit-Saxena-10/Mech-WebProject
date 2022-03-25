from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref
from flaskblog import db, login_manager
from flask_login import UserMixin
import enum

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class SubField(enum.Enum):
    TFE = 'TFE'
    Manufacturing = 'Manufacturing'
    Design = 'Design'

class Student_Program(enum.Enum):
    BTech = 'BTech'
    MTech = 'MTech'
    Phd = 'Phd'

class Section(enum.Enum):
    no_section = 'No Section'
    S1 = 'S1'
    S2 = 'S2'
    S3 = 'S3'


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=True)
    name = db.Column(db.String(60), nullable=True)
    field = db.Column(db.Enum(SubField), default=SubField.TFE, nullable=False)
    instructors = association_proxy('course_faculty', 'faculty')
    tas = association_proxy('course_ta', 'ta')

    def __repr__(self):
        return self.course_code


class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60),nullable = True)
    email = db.Column(db.String(30),unique=True, nullable=False)
    field = db.Column(db.Enum(SubField), default = SubField.TFE,nullable = False)
    courses = association_proxy('course_faculty','course')
    mail_confirmation = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return self.name


class Course_Faculty(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    section = db.Column(db.Enum(Section), default = Section.no_section,nullable = False)
    course = db.relationship(Course, backref=backref("course_faculty"))
    faculty = db.relationship(Faculty, backref=backref("course_faculty"))
    mail_confirmation = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return "course: "+str(self.course_id)+"  Faculty: "+ str(self.faculty_id)



class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    facad = db.Column(db.String(30), nullable=True)
    program = db.Column(db.Enum(Student_Program), default=SubField.TFE, nullable=False)
    field = db.Column(db.Enum(SubField), default=SubField.TFE, nullable=False)
    courses = association_proxy('course_ta', 'course')

    def __repr__(self):
        return f"Course('{self.id}', '{self.username}', '{self.email}', '{self.roll_number}', '{self.phone_number}', '{self.facad}')"

class Course_Ta(db.Model):

    id = db.Column('id', db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    section = db.Column(db.Enum(Section), default = Section.no_section,nullable = False)
    course = db.relationship(Course, backref=backref("course_ta"))
    ta = db.relationship(Student, backref=backref("course_ta"))
    

    def __repr__(self):
        return "course: "+str(self.course_id)+"  TA: "+ str(self.student_id)