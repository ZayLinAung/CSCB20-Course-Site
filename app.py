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

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        user_name = request.form['Username']
        email = request.form['Email']
        hashed_password = bcrypt.generate_password_hash(request.form['Password']).decode('utf-8')
        userType = request.form['userType']
        reg_details =(user_name,
                      email,
                      hashed_password, userType)
        add_users(reg_details)
        flash('registration successful! Please login now:')
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


@app.route('/assignments/instructor')
def assignments_instructor():
    return render_template('assignment.html')


@app.route('/feedback/student', methods = ['GET', 'POST'])
def feedback_student():
    if request.method == 'POST':
        f1 = request.form['f1']
        f2 = request.form['f2']
        f3 = request.form['f3']
        f4 = request.form['f4']
        
        
        flash('Feedback successfully submitted! ')
        return redirect(url_for('login'))
    else:
        return render_template('feedbackStudent.html')


@app.route('/feedback/instructor')
def feedback_instructor():
    return render_template('feedbackInstructor.html')


def add_users(reg_details):
      user = Person(username = reg_details[0], email = reg_details[1], password = reg_details[2], userType = reg_details[3])
      db.session.add(user)
      db.session.commit()


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')




#endpoint to create a regrade request for the user in session with 
#specified assignment_id
@app.route('/regrade/<assignment_id>', methods=['GET', 'POST'])
def requestRegrade(assignment_id):
    if request.method == 'GET':
        return render_template('regradeRequest.html', assignment_id = assignment_id)
    if request.method == 'POST':
        print("PRINTED OBJECT WOOHOO")
        regradeObj = Regrade_request(person_id = session['person_id'], assignment_id = assignment_id, 
                                    title= request.form['title'], content = request.form['content'],
                                    approved = False )
        #create a new regrade request 
        print("PRINTED OBJECT WOOHOO")
        db.session.add(regradeObj)
        db.session.commit()
        return render_template('regradeRequest.html', assignment_id = assignment_id)


#Helper function to get the all the grades belonging to a specific student.
def getAssignments(student_id):
    assignments = Grade.query.filter_by(person_id = student_id)
    return assignments


if __name__ == "__main__":
  app.run(debug=True)