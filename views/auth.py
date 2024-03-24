from flask import Flask, render_template, request, Blueprint
import sqlite3

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods = ['GET', 'POST'])
def register():
    
    if request.method == 'GET':
       return render_template('templates/register.html')
    
    if request.method == 'POST':
      con = sqlite3.connect("database.db")
      cur = con.cursor()
      cur.execute(
          "INSERT INTO User(username, password) VALUES (?, ?)", ("Zacky", "12345"),
      )
      con.commit()

      return '<h1>Hello, World!</h1>'