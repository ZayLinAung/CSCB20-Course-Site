from flask import Flask, render_template, request, flash, redirect, url_for, session, Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_bcrypt import bcrypt
from models.models import db

student_bp = Blueprint('student', __name__)

@student_bp.route('/feed', methods = ['GET'])
def feed():
    return render_template("student_feed.html")

@student_bp.route('/grades', methods = ['GET'])
def query_grades():
    list_of_grades = []
    return render_template("student_feed.html")