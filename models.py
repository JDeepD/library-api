from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Library(db.Model): #type: ignore
    ISBN = db.Column(db.String, primary_key = True, nullable=False)
    name = db.Column(db.String, index = True, nullable=False)
    author = db.Column(db.String, nullable=False)
    copies = db.Column(db.Integer, nullable=False)

    booked_by = db.Column(db.String, nullable=True)
    booked_on = db.Column(db.String, nullable=True)
    lend_by = db.Column(db.String, nullable=True)
    book_picked = db.Column(db.String, nullable=True)
    return_date = db.Column(db.String, nullable=True)
