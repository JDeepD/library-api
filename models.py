from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Library(db.Model): #type: ignore
    ISBN = db.Column(db.String, primary_key = True, nullable=False)
    name = db.Column(db.String, index = True, nullable=False)
    author = db.Column(db.String, nullable=False)
    copies = db.Column(db.Integer, nullable=False)
