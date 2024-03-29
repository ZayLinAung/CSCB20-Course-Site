from flask import Flask, render_template, request, flash, redirect, url_for, session, Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_bcrypt import bcrypt
from flask import Flask, render_template, request, flash, redirect, url_for, session, Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_bcrypt import bcrypt
from models.models import db, Student, Grade

student_bp = Blueprint('student', __name__)

@student_bp.route('/feed', methods = ['GET'])
def feed():
    return render_template("student_feed.html")



#G et all the grades associated with a user and send a response with the list
@student_bp.route('/grades', methods = ['GET'])
def query_grades():
    if request.method == 'GET':
        list_of_grades = Grade.query.filter_by(student_id=Student.id)
        return render_template("student_feed.html", grades=list_of_grades)
    
