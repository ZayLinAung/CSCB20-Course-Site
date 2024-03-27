from flask import Flask, render_template, request, flash, redirect, url_for, session, Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_bcrypt import bcrypt
from models.models import db

instructor_bp = Blueprint('instructor', __name__)

@instructor_bp.route('/feed', methods = ['GET'])
def feed():
    return render_template("instructor_feed.html")