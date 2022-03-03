from flaskblog import app, db
from flaskblog.models import Course, Student, User

if __name__ == '__main__':

    db.drop_all()
    db.create_all()
    user_1 = User(username='admin1', email='admin1@iitb.ac.in', password='admin1', role='admin')
    user_2 = User(username='admin2', email='admin2@iitb.ac.in', password='admin2', role='admin')
    user_3 = User(username='student1', email='student1@iitb.ac.in', password='student1', role='student')
    user_4 = User(username='student2', email='student2@iitb.ac.in', password='student2', role='student')
    course_1 = Course(course_code='ME001', course_name='Mech001')
    course_2 = Course(course_code='ME002', course_name='Mech002')
    student_1 = Student(username='student1', email='student1@iitb.ac.in', password='student1',
                        roll_number='1', phone_number='1234567890', facad='FacultyAdvisor1', role='student')
    student_2 = Student(username='student2', email='student2@iitb.ac.in', password='student2',
                        roll_number='2', phone_number='2345678901', facad='FacultyAdvisor2', role='student')
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.add(user_3)
    db.session.add(user_4)
    db.session.add(course_1)
    db.session.add(course_2)
    db.session.add(student_1)
    db.session.add(student_2)
    db.session.commit()

    # Start App
    app.run(debug=True)