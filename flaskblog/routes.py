from flask import render_template, url_for, flash, redirect, request, jsonify
from flaskblog.models import  User, Course, SubField, Course_Faculty, Course_Ta, Section, Faculty, Student, Student_Program
from flaskblog.forms import LoginForm
from flaskblog import app, bcrypt, db, mail
from flask_login import login_required, login_user, current_user, logout_user
import json 
from flask_mail import Message

@app.route("/")
@app.route("/home")
def home():
    courses = Course.query.all()
    return render_template('home.html', courses=courses)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if user and bcrypt.check_password_hash(user.password, form.password.data):
        if user and user.password == form.password.data :
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


@app.route("/course/<int:course_id>")
def course(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course.html', title=course.code, course=course)

# Allotment 

@app.route("/allotment", methods=['GET', 'POST'])
@login_required
def allotment():
    fields = [field.value for field in SubField]
    courses = Course.query.all()
    course_facultys = Course_Faculty.query.all()
    return render_template('allotment.html', title='Allotment',
                            courses=courses, fields=fields, course_facultys=course_facultys)


@app.route("/Coursefaculty/<int:id>/<int:action>", methods=['GET', 'POST'])
@login_required
def delete_entry(id, action):
    if action == 0:
        faculty = Faculty.query.filter_by(id=id).first()
        faculty.mail_confirmation = False
    if action == 1:
        course_faculty = Course_Faculty.query.filter_by(id=id).first()
        db.session.delete(course_faculty)
    db.session.commit()
   
    return redirect(url_for('allotment'))


@app.route("/course", methods = ["GET","POST"])
@login_required
def get_course():
    subfield = request.form.get('subfield')
    courses_query = Course.query.filter_by(field=subfield)
    courses = [{'id':course.id,'name':course.name} for course in courses_query]
    return jsonify(courses)


@app.route("/alloted_sections", methods = ["GET","POST"])
@login_required
def get_alloted_sections():
    course_id = request.form.get('course_id')
    query = Course_Faculty.query.filter_by(course_id=course_id)
    course_sections = [{'section':q.section.value,'prof':q.faculty.name} for q in query]
    return jsonify(course_sections)


@app.route("/get_fac", methods = ["GET","POST"])
@login_required
def get_fac():
    subfield,course_id,num_sections = request.form.get('subfield'),request.form.get('course_id'),int(request.form.get('num_sections'))
    query = Course_Faculty.query.filter_by(course_id=course_id)
    course_sections = [q.section.value for q in query]
    course_sections.append(Section.no_section.value)  # Adding this in course sections so that No_section is not added as a section later
    # get new sections that are to be alloted
    new_sections = [section.value for section in Section if section.value not in course_sections]
    faculty = [{'name':fac.name,'id':fac.id} for fac in Faculty.query.filter(Faculty.field.in_([subfield]))]
    response = {'sections':new_sections[:num_sections],'profs':faculty}
    # Get next sections
    return jsonify(response)


@app.route("/allot_section_fac", methods = ["GET","POST"])
@login_required
def allot_section_fac():
    section_faculty_list = json.loads(request.form.get('section_faculty_list'))
    course_id = request.form.get('course_id')
    for ta in section_faculty_list:
        section,faculty_id = ta['section'],ta['faculty_id']
        q = Course_Faculty.query.filter_by(faculty_id=faculty_id,course_id=course_id)
        if q.count()==0:
            if faculty_id:
                new_entry = Course_Faculty(faculty_id=faculty_id,course_id=course_id,section=section)
                db.session.add(new_entry)
    db.session.commit()
    return jsonify([])


def send_mails(email_list):
    for email in email_list:
        email = str(email)
        faculty = Faculty.query.filter_by(email=email).first()
        if faculty:
            if faculty.mail_confirmation == False:
                email_ = [email]
                body_ = "Hello Professor" + str(faculty.name) + ".You have been assigned courses " + str(faculty.courses)
                message = Message(subject="Test Mail", recipients=email_, 
                                    body = body_ , sender= "sender@gmail.com" )
                #mail.send(message)
                faculty.mail_confirmation = True
    db.session.commit()


@app.route("/send_multiple_mail", methods=['GET', 'POST'])
@login_required
def send_multiple_mail():
    course_tas = Course_Faculty.query.all()
    email_list = []
    for course_faculty in course_tas:
        if course_faculty.faculty.mail_confirmation == False:
            email_list.append(course_faculty.faculty.email)
    send_mails(email_list)
    flash(str(len(email_list))+' Mails Have been sent', 'success')
    return redirect(url_for('allotment'))


@app.route("/ta_allotment/<int:faculty_id>")
def ta_allot(faculty_id):
    faculty = Faculty.query.filter_by(id=faculty_id)[0]
    course_query = Course_Faculty.query.filter_by(faculty_id=faculty_id)
    course_ta = Course_Ta.query.all()
    print('courses here')
    for course in course_query:
        print(course.course_id,course.faculty_id)
    student_query = Student.query.filter_by(field=faculty.field)
    

    courses = [{'id':c.course.id,'code':c.course.code,'name':c.course.name, 'section':c.section.value} for c in course_query]
    students = [{'id':student.id,'name':student.name} for student in student_query]
    ta = [{'student_id':c.student_id, 'course_id':c.course_id, 'section':c.section.value} for c in course_ta]
    print(courses)
    print(students)
    print(ta)
    return render_template('ta_allotment.html', courses=courses, course_ta=course_ta, students=students,faculty={'name':faculty.name,'id':faculty.id})

@app.route("/allot_ta_fac", methods = ["GET","POST"])
def allot_ta_fac():
    ta_list = json.loads(request.form.get('ta_list'))
    faculty_id = request.form.get('faculty_id')

    for ta in ta_list:
        course_id,section,student_id = ta['course_id'],ta['section'],ta['student_id']    
        entry = Course_Ta(course_id=course_id, student_id=student_id, section=section)
        course_faculty = Course_Faculty.query.filter_by(course_id=course_id, faculty_id=faculty_id)
        student = Student.query.filter_by(id=student_id).first()
        if course_faculty:
            db.session.add(entry)
            if student.alloted!=0:
                flash(str(student.name)+" has already been alloted under other course", "info")
            student.alloted +=1
    db.session.commit()
    return jsonify([])

@app.route("/ta_allot_delete/<int:fac_id>/<int:id>", methods=['GET', 'POST'])
def ta_allot_delete(id, fac_id):
    course_ta = Course_Ta.query.filter_by(id=id).first()
    db.session.delete(course_ta)
    course_ta.ta.alloted -=1
    db.session.commit()
    return redirect(url_for('ta_allot',faculty_id = fac_id))


@app.route("/student_allotment", methods=['GET', 'POST'])
@login_required
def student_allotment():
    fields = [field.value for field in SubField]
    courses = Course.query.all()
    course_tas = Course_Ta.query.all()
    return render_template('student_allotment.html', title='Allotment',
                            courses=courses, fields=fields, course_tas=course_tas)


@app.route("/delete_ta_entry/<int:id>", methods=['GET', 'POST'])
def delete_ta_entry(id):
    course_ta = Course_Ta.query.filter_by(id=id).first()
    db.session.delete(course_ta)
    course_ta.ta.alloted -=1
    db.session.commit()
    return redirect(url_for('student_allotment'))