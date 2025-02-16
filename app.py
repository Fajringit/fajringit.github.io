# app.py
from flask import Flask, request, jsonify
from db_config import get_db_connection

app = Flask(__name__)

# Create User
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;",
        (data['name'], data['email'])
    )
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": user_id, "message": "User created"}), 201

# Get All Users
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": u[0], "name": u[1], "email": u[2]} for u in users])

# Get User by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users WHERE id = %s;", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return jsonify({"id": user[0], "name": user[1], "email": user[2]})
    return jsonify({"error": "User not found"}), 404

# Update User
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET name = %s, email = %s WHERE id = %s RETURNING id;",
        (data['name'], data['email'], user_id)
    )
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if updated:
        return jsonify({"message": "User updated"})
    return jsonify({"error": "User not found"}), 404

# Delete User
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s RETURNING id;", (user_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if deleted:
        return jsonify({"message": "User deleted"})
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
