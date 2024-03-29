from flask import Flask, render_template, request, flash, redirect, url_for, session, Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from views.instructors import instructor_bp
from views.students import student_bp
from models.models import db



app = Flask(__name__)
bcrypt = Bcrypt(app)

#Config things
app.config['SECRET_KEY']='8a0f946f1471e113e528d927220ad977ed8b2cce63303beff10c8cb4a15e1a99'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10)




@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

from views.auth import auth_bp

app.register_blueprint(auth_bp, url_prefix = '/auth')
app.register_blueprint(instructor_bp, url_prefix = '/instructor');
app.register_blueprint(student_bp, url_prefix = '/student');

db.init_app(app)

if __name__ == "__main__":

  app.run()