from flask import Flask, render_template, request, flash, redirect, url_for, session, Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
import models

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        user_name = request.form['Username']
        email = request.form['Email']
        hashed_password=bcrypt.generate_password_hash(request.form['Password']).decode('utf-8')
        userType = request.form['Type']
        reg_details =(user_name,
                      email,
                      hashed_password, userType)
        # add_users(reg_details)
        flash('registration successful! Please login now:')
        return redirect(url_for('login'))
    
@auth_bp.route('/login', methods = ['GET', 'POST'])
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

@auth_bp.route('/logout')
def logout():
    session.pop('name', default = None)
    return redirect(url_for('home'))


# def add_users(reg_details):
#     user = Person(username = reg_details[0], email = reg_details[1], password = reg_details[2])
#     db.session.add(user)
#     db.session.commit()