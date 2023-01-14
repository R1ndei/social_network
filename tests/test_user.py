import pytest
import json

register_user_data: dict = {
    "phone": "79113559292",
    "email": "test.testmail@gmail.com",
    "password": "testpass123",
    "first_name": "Tester",
    "last_name": "Tester",
    "mid_name": "Tester"
}

register_user_without_posts_data: dict = {
    "phone": "79113219494",
    "email": "test.testmailwithout@gmail.com",
    "password": "testpass123",
    "first_name": "Tester2",
    "last_name": "Tester2",
    "mid_name": "Tester2"
}

register_user_data_incorrect_email: dict = {
    "phone": "79113559292",
    "email": "test.testmail.com",
    "password": "testpass123",
    "first_name": "Tester",
    "last_name": "Tester",
    "mid_name": "Tester"
}

register_user_data_incorrect_phone: dict = {
    "phone": "791135592",
    "email": "test.testmail.com",
    "password": "testpass123",
    "first_name": "Tester",
    "last_name": "Tester",
    "mid_name": "Tester"
}

register_user_data_small_pass: dict = {
    "phone": "79113559292",
    "email": "test.testmail@gmail.com",
    "password": "tes23",
    "first_name": "Tester",
    "last_name": "Tester",
    "mid_name": "Tester"
}


@pytest.mark.asyncio()
async def test_register_user(apply_migrations, async_client):
    response = await async_client.post("/api/v1/authorization/registration", json=register_user_data)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["status"] == 200
    assert response_json["value"] == register_user_data["email"]


@pytest.mark.asyncio()
async def test_register_user_without_posts(async_client):
    response = await async_client.post("/api/v1/authorization/registration", json=register_user_without_posts_data)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["status"] == 200
    assert response_json["value"] == register_user_without_posts_data["email"]


@pytest.mark.asyncio()
async def test_register_user_incorrect_email(async_client):
    response = await async_client.post("/api/v1/authorization/registration", json=register_user_data_incorrect_email)
    response_json = response.json()
    assert response.status_code == 422
    assert response_json['detail'][0]['type'] == "value_error.email"


@pytest.mark.asyncio()
async def test_register_user_incorrect_phone(async_client):
    response = await async_client.post("/api/v1/authorization/registration", json=register_user_data_incorrect_phone)
    response_json = response.json()
    assert response.status_code == 400
    assert response_json['detail'] == "Please enter a valid phone number"


@pytest.mark.asyncio()
async def test_register_user_small_pass(async_client):
    response = await async_client.post("/api/v1/authorization/registration", json=register_user_data_small_pass)
    response_json = response.json()
    assert response.status_code == 400
    assert response_json['detail'] == "Password must be at least 7 characters long"


@pytest.mark.asyncio()
async def test_login_user(async_client):
    payload = {"username": register_user_data['email'], "password": register_user_data["password"]}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'accept': 'application/json'
    }
    response = await async_client.post("/api/v1/authorization/login", headers=headers, data=payload)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['access_token']
    assert response_json["token_type"] == "bearer"
