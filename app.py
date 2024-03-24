from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
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
    
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO User(username, password) VALUES (?, ?)", ("Zacky", "12345"),
    )
    con.commit()

    return '<h1>Hello, World!</h1>'


if __name__ == "__main__":
  app.run()