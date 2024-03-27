from flask import Flask, render_template, request, flash, redirect, url_for, session, Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from views.auth import auth_bp

app = Flask(__name__)

bcrypt=Bcrypt(app)

app.config['SECRET_KEY']='8a0f946f1471e113e528d927220ad977ed8b2cce63303beff10c8cb4a15e1a99'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10)



@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

app.register_blueprint(auth_bp, url_prefix = '/auth')

if __name__ == "__main__":
  app.run()