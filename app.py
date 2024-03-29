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

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        user_name = request.form['Username']
        email = request.form['Email']
        hashed_password = bcrypt.generate_password_hash(request.form['Password']).decode('utf-8')
        userType = request.form['userType']
        print(type(userType))
        reg_details =(user_name,
                      email,
                      hashed_password, userType)
        add_users(reg_details)
        flash('registration successful! Please login now:')
        return redirect(url_for('login'))


@app.route('/registerinstructor', methods = ['GET', 'POST'])
def register_instructor():    
    if request.method == 'GET':
        return render_template('register.html');
    else:
        username = request.form['Username']
        password = request.form['Password']
        instructor = instructor.query.filter_by(username = username).first()


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
            return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('name', default = None)
    return redirect(url_for('home'))


def add_users(reg_details):
      user = Person(username = reg_details[0], email = reg_details[1], password = reg_details[2], userType = reg_details[3])
      db.session.add(user)
      db.session.commit()


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

# @app.route('/feed', methods = ['GET'])
# def feed():
#     return render_template("student_feed.html")



#G et all the grades associated with a user and send a response with the list
# @app.route('/grades', methods = ['GET'])
# def query_grades():
#     if request.method == 'GET':
#         list_of_grades = Grade.query.filter_by(student_id=Student.id)
#         return render_template("student_feed.html", grades=list_of_grades)
    
# @app.route('/feed', methods = ['GET'])
# def feed():
#     return render_template("instructor_feed.html")

@app.route('/grades/<student>', methods = ['GET'])
def grades(student):
    return

if __name__ == "__main__":
  app.run(debug=True)