from flask import Flask, render_template, request
import sqlite3

from flask_sqlalchemy import SQLAlchemy
from views.auth import auth_bp

app = Flask(__name__)

db = SQLAlchemy(app)
conn = sqlite3.connect("database.db")

conn.execute(
    """
    CREATE TABLE IF NOT EXISTS User 
    (
        id INTEGER PRIMARY KEY,
        username TEXT, 
        password TEXT
    )
    """
)

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

app.register_blueprint(auth_bp, url_prefix = '/auth')

if __name__ == "__main__":
  app.run()