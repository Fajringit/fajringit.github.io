import requests
import time

BASE_URL = "http://127.0.0.1:5000/users"

# 0. Health Check (Sebelum Tes Utama)
def test_health_check():
    response = requests.get("http://127.0.0.1:5000/health")
    assert response.status_code == 200, f"API Health Check Failed: {response.status_code}"

# 1. POST - Create User
def test_create_user():
    payload = {"name": "John", "email": "john@example.com"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(BASE_URL, json=payload, headers=headers)
    assert response.status_code == 201, f"Create User Failed: {response.status_code}"

# 2. GET - Get All Users
def test_get_users():
    response = requests.get(BASE_URL)
    assert response.status_code == 200, "Expected 200"

# 3. GET - Get User by ID
def test_get_user_by_id():
    user_id = 1  # Sesuaikan ID dengan yang ada
    response = requests.get(f"{BASE_URL}/{user_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print(f"User {user_id}:", response.json())

# 4. PUT - Update User
def test_update_user():
    user_id = 1
    data = {"name": "Fajrin", "email": "updated@example.com"}
    response = requests.put(f"{BASE_URL}/{user_id}", json=data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print(f"User {user_id} updated:", response.json())

# 5. DELETE - Delete User
def test_delete_user():
    user_id = 1
    response = requests.delete(f"{BASE_URL}/{user_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print(f"User {user_id} deleted:", response.json())

# Jangan panggil fungsi secara langsung di luar blok Pytest
if __name__ == "__main__":
    print("Jalankan tes dengan `pytest test_api.py`")
