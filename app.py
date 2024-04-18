from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)

#Config things
app.config['SECRET_KEY']='8a0f946f1471e113e528d927220ad977ed8b2cce63303beff10c8cb4a15e1a99'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10)
db = SQLAlchemy(app)


# databases
class Person(db.Model):
    __tablename__ = 'Person'
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(25), unique=False, nullable=False)
    userType = db.Column(db.String(25), unique=False, nullable=False)

    def __repr__(self):
        return f"Student('{self.username}', '{self.email}')"


class Assignment(db.Model):
    __tablename__ = 'Assignment'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False, nullable=False)
    content = db.Column(db.String(2000), unique=False, nullable=False)
    total = db.Column(db.Integer, unique=False, nullable=False)
    grades = db.relationship('Grade', backref='assignment', lazy=True)


class Grade(db.Model):
    __tablename__ = 'Grade'
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('Assignment.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('Person.id'), nullable=False)
    result = db.Column(db.Integer, unique=False, nullable=False)


class Regrade_request(db.Model):
    __tablename__ = 'Regrade'
    id=db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('Person.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('Assignment.id'), nullable=False)
    title = db.Column(db.String(200), unique=False, nullable=False)
    content = db.Column(db.String(2000), unique=False, nullable=False)
    approved = db.Column(db.Boolean, default = False)
    


class Feedback(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('Person.id'), nullable=False)
    f1 = db.Column(db.String(200), unique=False, nullable=True)
    f2 = db.Column(db.String(200), unique=False, nullable=True)
    f3 = db.Column(db.String(200), unique=False, nullable=True)
    f4 = db.Column(db.String(200), unique=False, nullable=True)



@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        user_name = request.form['Username']
        person = Person.query.filter_by(username = user_name).first()
        if person:
            flash('Username Already Exist. Try again!', 'Error')
            return render_template('register.html')

        email = request.form['Email']
        person = Person.query.filter_by(email = email).first()
        if person:
            flash('Email Already Exist. Try again!', 'Error')
            return render_template('register.html')
        if request.form['Password'] != request.form['confirmPassword']:
            flash('Please confirm your password matches. Try again!', 'Error')
            return render_template('register.html')
        
        hashed_password = bcrypt.generate_password_hash(request.form['Password']).decode('utf-8')
        userType = request.form['userType']
        print(type(userType))
        reg_details =(user_name,
                      email,
                      hashed_password, userType)
        add_users(reg_details)
        flash('Registration successful! Please login now:')
        return redirect(url_for('login'))


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'name' in session:
            flash('You Already logged in!')
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    else:
        username = request.form['Username']
        password = request.form['Password']
        person = Person.query.filter_by(username = username).first()
        if not person or not bcrypt.check_password_hash(person.password, password):
            flash('Please check your login details and try again.', 'error')
            return render_template('login.html')
        else:
            log_details = (
            username,
            password
            )
            session['name']=username
            session.permanent=True
            session['person_id'] = person.id
            session['userType'] = person.userType
            return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('name', default = None)
    return redirect(url_for('home'))


@app.route('/assignments/student')
def assignments_student():
    student_assignments = getAssignments(student_id=session['person_id'])
    return render_template('student_feed.html', assignments_query = student_assignments)

@app.route('/regrade/instructor')
def regrade_instructor():
    regradeQuery = getRegrade()
    return render_template('instructor_regrade.html', all_regrades = regradeQuery)

@app.route('/assignments/instructor')
def assignments_instructor():
   
    return render_template('assignment.html')

@app.route('/A1_grades/assignments/instructor/')
def instructor_A1_grades():

    assignment = Assignment.query.get(1)
    total_A1 = assignment.total
    all_grades = Grade.query.filter_by(assignment_id=1).all()
    all_person_ids = [grade.person_id for grade in all_grades]
    persons = Person.query.filter(Person.id.in_(all_person_ids)).all()
    usernames = [person.username for person in persons]
    grades_names = zip(all_grades, usernames)

    return render_template('instructor_A1_grades.html', grades_names=grades_names, total=total_A1)

@app.route('/A2_grades/assignments/instructor/')
def instructor_A2_grades():

    
    assignment = Assignment.query.get(2)
    total_A2 = assignment.total
    all_grades = Grade.query.filter_by(assignment_id=2).all()
    all_person_ids = [grade.person_id for grade in all_grades]
    persons = Person.query.filter(Person.id.in_(all_person_ids)).all()
    usernames = [person.username for person in persons]
    grades_names = zip(all_grades, usernames)

    return render_template('instructor_A2_grades.html', grades_names=grades_names, total=total_A2)

@app.route('/A3_grades/assignments/instructor/')
def instructor_A3_grades():

    assignment = Assignment.query.get(3)
    total_A3 = assignment.total
    all_grades = Grade.query.filter_by(assignment_id=3).all()
    all_person_ids = [grade.person_id for grade in all_grades]
    persons = Person.query.filter(Person.id.in_(all_person_ids)).all()
    usernames = [person.username for person in persons]
    grades_names = zip(all_grades, usernames)

    return render_template('instructor_A3_grades.html', grades_names=grades_names, total=total_A3)

@app.route('/update_gradeA1', methods=['POST'])
def update_grade_A1():
    grade_id = request.form['grade_id']
    new_grade = request.form['new_grade']
    grade = Grade.query.get(grade_id) 
    grade.result = new_grade
    db.session.commit()
    return redirect(url_for('instructor_A1_grades'))

@app.route('/update_gradeA2', methods=['POST'])
def update_grade_A2():
    grade_id = request.form['grade_id']
    new_grade = request.form['new_grade']
    grade = Grade.query.get(grade_id) 
    grade.result = new_grade
    db.session.commit()
    return redirect(url_for('instructor_A2_grades'))

@app.route('/update_gradeA3', methods=['POST'])
def update_grade_A3():
    grade_id = request.form['grade_id']
    new_grade = request.form['new_grade']
    grade = Grade.query.get(grade_id) 
    grade.result = new_grade
    db.session.commit()
    return redirect(url_for('instructor_A3_grades'))





@app.route('/feedback/student', methods = ['GET', 'POST'])
def feedback_student():
    if request.method == 'POST':
        f1 = request.form['f1']
        f2 = request.form['f2']
        f3 = request.form['f3']
        f4 = request.form['f4']
        instructor_id = request.form['instructor']
        
        newFeedback = Feedback(instructor_id = instructor_id, f1 = f1, f2 = f2, f3 = f3, f4 = f4)
        db.session.add(newFeedback)
        db.session.commit()
        flash('Feedback successfully submitted!')
        return redirect(url_for('feedback_student'))
    else:
        person = Person.query.filter_by(userType = 'Instructor').all()
        return render_template('feedbackStudent.html', instructors = person)


@app.route('/feedback/instructor')
def feedback_instructor():
    feedbacks = Feedback.query.filter_by(instructor_id = session['person_id']).all()
    return render_template('feedbackInstructor.html', feedbacks = feedbacks)


def add_users(reg_details):
      user = Person(username = reg_details[0], email = reg_details[1], password = reg_details[2], userType = reg_details[3])
      db.session.add(user)
      db.session.commit()


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')


@app.route('/labs')
def labs():
    return render_template('labs.html')


@app.route('/resources')
def resources():
    return render_template('resources.html')


@app.route('/lectures')
def lectures():
    return render_template('lecture.html')


@app.route('/courseTeam')
def courseTeam():
    return render_template('courseTeam.html')




#endpoint to create a regrade request for the user in session with 
#specified assignment_id
@app.route('/regrade/<assignment_id>', methods=['GET', 'POST'])
def requestRegrade(assignment_id):
    if request.method == 'GET':
        return render_template('regradeRequest.html', assignment_id = assignment_id)
    if request.method == 'POST':
        print("PRINTED OBJECT WOOHOO")
        AssignmentName = Assignment.query.filter_by(id=assignment_id).first().title
        regradeObj = Regrade_request(person_id = session['person_id'], assignment_id = assignment_id, 
                                    title= request.form['title'], content = request.form['content'],
                                    approved = False)
        #create a new regrade request 
        print("PRINTED OBJECT WOOHOO")
        db.session.add(regradeObj)
        db.session.commit()
        return render_template('regradeRequest.html', assignment_id = assignment_id)


#Helper function to get the all the grades belonging to a specific student.
def getAssignments(student_id):
    assignments = Grade.query.filter_by(person_id = student_id)
    return assignments


def getRegrade():
    all_regrades = Regrade_request.query.all()
    return all_regrades


if __name__ == "__main__":
  app.run(debug=True)