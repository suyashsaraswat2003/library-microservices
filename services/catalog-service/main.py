from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
BOOK_SERVICE_URL = "http://book-service:8000"

@app.route("/search", methods=["GET"])
def search_books():
    author = request.args.get("author")
    genre = request.args.get("genre")

    resp = requests.get(f"{BOOK_SERVICE_URL}/books")
    books = resp.json()

    if author:
        books = [b for b in books if author.lower() in b["author"].lower()]
    if genre:
        books = [b for b in books if genre.lower() in b["genre"].lower()]
    return jsonify(books)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003)
