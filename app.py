# app.py
from flask import Flask, request, jsonify
import traceback
from db_config import get_db_connection
import logging

app = Flask(__name__)

# Tambahkan logging
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

@app.before_request
def log_request_info():
    logging.info(f"Request: {request.method} {request.url} - Data: {request.get_json()}")

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Error: {e}")
    traceback.print_exc()
    return jsonify({"error": str(e)}), 500


# Health Check
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        if not data.get('name') or not data.get('email'):
            return jsonify({"error": "Name and email required"}), 400
        
        # Contoh log input
        print(f"Received data: {data}")

        # Simulasi insert ke database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;",
            (data['name'], data['email'])
        )
        new_user_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"id": new_user_id, "name": data['name'], "email": data['email']}), 201
    
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()  # Lihat error lengkap di log
        return jsonify({"error": "Internal Server Error"}), 500


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

if __name__ == "__main__":
    print("🚀 Starting Flask server on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
