from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
books = []

@app.route("/books", methods=["GET"])
def list_books():
    return jsonify(books)

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return jsonify(book)
    abort(404, "Book not found")

@app.route("/books", methods=["POST"])
def add_book():
    book = request.get_json()
    book["available"] = True
    book["borrowed_by"] = None
    books.append(book)
    return jsonify(book), 201

@app.route("/books/<int:book_id>", methods=["PATCH"])
def update_book(book_id):
    data = request.get_json()
    for book in books:
        if book["id"] == book_id:
            book.update(data)
            return jsonify(book)
    abort(404, "Book not found")

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return jsonify({"message": "Book deleted successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
