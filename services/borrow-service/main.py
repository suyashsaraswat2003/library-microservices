from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
BOOK_SERVICE_URL = "http://book-service:8000"
USER_SERVICE_URL = "http://user-service:8001"

borrowed_records = []

@app.route("/borrow", methods=["POST"])
def borrow_book():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        book_id = data.get("book_id")

        # Validate user
        user_resp = requests.get(f"{USER_SERVICE_URL}/users/{user_id}")
        if user_resp.status_code != 200:
            return jsonify({"error": "User not found"}), 404

        # Validate book
        book_resp = requests.get(f"{BOOK_SERVICE_URL}/books/{book_id}")
        if book_resp.status_code != 200:
            return jsonify({"error": "Book not found"}), 404

        book = book_resp.json()
        if not book.get("available", True):
            return jsonify({"error": "Book is currently unavailable"}), 400

        # Mark book as borrowed
        patch_resp = requests.patch(f"{BOOK_SERVICE_URL}/books/{book_id}", json={
            "available": False,
            "borrowed_by": user_id
        })
        if patch_resp.status_code != 200:
            return jsonify({"error": "Failed to update book"}), 500

        borrowed_records.append({"user_id": user_id, "book_id": book_id})
        return jsonify({"message": "Book borrowed successfully"})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/return", methods=["POST"])
def return_book():
    data = request.get_json()
    user_id = data.get("user_id")
    book_id = data.get("book_id")

    global borrowed_records
    borrowed_records = [r for r in borrowed_records if not (r["user_id"]==user_id and r["book_id"]==book_id)]

    # Mark book as available
    requests.patch(f"{BOOK_SERVICE_URL}/books/{book_id}", json={
        "available": True,
        "borrowed_by": None
    })

    return jsonify({"message": "Book returned successfully"})

@app.route("/borrowed", methods=["GET"])
def get_borrowed():
    return jsonify(borrowed_records)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)
