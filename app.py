import sys
from flask import Flask, jsonify, request
from models import db, Library # type: ignore

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
    db.init_app(app)
    return app

app = create_app()
db.init_app(app)

@app.route("/")
def intro():
    return "Hello World"

@app.route("/<string:name>")
def get_book(name):
    book = Library.query.filter(Library.name.contains(name)).all()
    data = []
    for dats in book:
        atom = {
            "ISBN" : dats.ISBN,
            "name" : dats.name,
            "author" : dats.author,
            "copies" : dats.copies,
            "cover_url" : dats.cover_url,
        }
        data.append(atom)

    resp = jsonify(data)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp



@app.route("/delete/<ISBN>")
def delete_book(ISBN):
    book = Library.query.filter(Library.ISBN == ISBN).first()
    try:
        db.session.delete(book)
        db.session.commit()
        response = jsonify({"message" : "deleted"})
        response.status = 201
        return response
    except:
        response = jsonify({"message" : "error"})
        response.status = 400 
        return response

@app.route("/add/", methods=["POST"])
def add_book():
    ISBN = request.form.get("ISBN")
    name = request.form.get("name")
    author = request.form.get("author")
    copies = request.form.get("copies")
    cover_url = request.form.get("cover_url")

    if not all((ISBN, name, author, copies, cover_url)):
        return "Missing args\n", 400 

    book = Library(ISBN = ISBN, name=name, author=author, copies=copies, cover_url=cover_url)
    db.session.add(book)
    db.session.commit()

    response = jsonify({"message" : "success"})
    response.status_code = 201
    return response

if __name__ == "__main__":
    if "createdb" in sys.argv:
        with app.app_context():
            db.create_all()
        print("Database created")
    elif "seeddb" in sys.argv:
        with app.app_context():
            book = Library(ISBN = "111-222-222", name="Sherlock", author = "JJ", copies=4, cover_url="sherlock.jpg")
            db.session.add(book)
            db.session.commit()
        print("Database seeded with 1 entry")
    else:
        app.run(debug=True)
