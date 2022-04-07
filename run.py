from flaskblog import app, db, bcrypt
from flaskblog.models import Course, Student, User, Faculty, Course_Faculty, Course_Ta

if __name__ == '__main__':

    db.drop_all()
    db.create_all()
    user= User(username='admin', email='admin@iitb.ac.in', password='admin')
    # user.password = bcrypt.generate_password_hash(user.password).decode('utf-8')
    c1 = Course(code="ME219", name = 'Fluid',field='TFE')
    c2 = Course(code="ME222", name = 'Manpro',field='Manufacturing')
    c3 = Course(code="ME209", name = 'Thermo',field='TFE')
    c4 = Course(code="ME224", name = 'squid',field='Design')
    c5 = Course(code="ME223", name = 'pro',field='Manufacturing')
    c6 = Course(code="ME200", name = 'Thermodynamics',field='Design')
    
    f1 = Faculty(name = 'f1',email="f1@iitb.ac.in",field='TFE')
    f2 = Faculty(name = 'f2',email="f2@iitb.ac.in",field='TFE')
    f3 = Faculty(name = 'f3',email="f3@iitb.ac.in",field='Manufacturing')
    f6 = Faculty(name = 'f6',email="f6@iitb.ac.in",field='Design')
    s1 = Student(name='student1',email="s1@iitb.ac.in",
                roll_number="1",phone_number="XXXXX12345",
                program = 'MTech',field='TFE')
    s2 = Student(name='student2',email="s2@iitb.ac.in",
                roll_number="2",phone_number="XXXXX22345",
                program = 'MTech',field='TFE')
    s3 = Student(name='student3',email="s3@iitb.ac.in",
                roll_number="3",phone_number="XXXXX32345",
                program = 'MTech',field='Manufacturing')
    s4 = Student(name='student4',email="s4@iitb.ac.in",
                roll_number="4",phone_number="XXXXX42345",
                program = 'MTech',field='Design')
    db.session.add(user)
    db.session.add_all([c1,c2,c3,c4,c5,c6,f1,f2,f3,f6,s1,s2,s3])
    db.session.commit()
    db.session.commit()

    # Start App
    app.run(debug=True)