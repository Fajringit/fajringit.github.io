import requests

BASE_URL = "http://127.0.0.1:5000/users"

# 1. POST - Create User
def test_create_user():
    data = {"name": "Fajrin", "email": "fajrin@example.com"}
    response = requests.post(BASE_URL, json=data)
    assert response.status_code == 201
    print("Create User:", response.json())

# 2. GET - Get All Users
def test_get_users():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    print("All Users:", response.json())

# 3. GET - Get User by ID
def test_get_user_by_id(user_id):
    response = requests.get(f"{BASE_URL}/{user_id}")
    assert response.status_code == 200
    print(f"User {user_id}:", response.json())

# 4. PUT - Update User
def test_update_user(user_id):
    data = {"name": "Fajrin Updated", "email": "fajrin.updated@example.com"}
    response = requests.put(f"{BASE_URL}/{user_id}", json=data)
    assert response.status_code == 200
    print(f"User {user_id} updated:", response.json())

# 5. DELETE - Delete User
def test_delete_user(user_id):
    response = requests.delete(f"{BASE_URL}/{user_id}")
    assert response.status_code == 200
    print(f"User {user_id} deleted:", response.json())

if __name__ == "__main__":
    test_create_user()  # Test Create User
    test_get_users()    # Test Get All Users
    test_get_user_by_id(4)  # Test Get User by ID (assumes ID 1 exists)
    test_update_user(4)  # Test Update User (assumes ID 1 exists)
    test_delete_user(4)  # Test Delete User (assumes ID 1 exists)
