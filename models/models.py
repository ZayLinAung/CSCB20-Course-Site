from flask_sqlalchemy import SQLAlchemy
#Create database
db = SQLAlchemy()



class Student(db.Model):
    __tablename__ = 'Student'
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(25), unique=False, nullable=False)
    # grades_list = db.relationship('Grade', lazy='select',
    #     backref=db.backref('student', lazy='joined'))
    

    
    def __repr__(self):
        return f"Student('{self.username}', '{self.email}')"


class Instructor(db.Model):
    __tablename__ = 'Instructor'
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(25), unique=False, nullable=False)


class Assignment(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False, nullable=False)
    content = db.Column(db.String(2000), unique=False, nullable=False)
    total=db.Column(db.Integer, unique = False, nullable=False)


class Grade(db.Model):
    __tablename__ = 'Grade'
    id=db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('Student.id'), nullable=False)
    result=db.Column(db.Integer, unique = False, nullable=False)


class regrade_request(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    title = db.Column(db.String(200), unique=False, nullable=False)
    content = db.Column(db.String(2000), unique=False, nullable=False)
    approved = db.Column(db.Boolean, default = False)
    



    
