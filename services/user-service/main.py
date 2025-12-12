from flask import Flask, jsonify, request, abort
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
users = []

@app.route("/users", methods=["GET"])
def list_users():
    return jsonify(users)

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    for u in users:
        if u["id"] == user_id:
            return jsonify(u)
    abort(404, "User not found")

@app.route("/users", methods=["POST"])
def add_user():
    user = request.get_json()
    users.append(user)
    return jsonify(user), 201

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message": "User deleted successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
