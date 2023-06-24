from main import app
from fastapi import Response, HTTPException
from fastapi.testclient import TestClient


client = TestClient(app)


def test_create_user():
    user_data = {
        "username": "test",
        "password": "test12345",
        "email": "test@gmail.com",
        "first_name": "test",
        "last_name": "test",
        "is_active": True,
    }
    
    response : Response = client.post('/auth/user',json=user_data)
    assert response.status_code == 200 or 409
    assert response.json() == {"response": "Registration was successful!"} or {'error':'Username already taken!'}