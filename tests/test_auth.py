from tests.conftest import client


async def test_login_handler(admin_user):
    admin, user_data, password = admin_user
    data = {
            "login": user_data["email"], "password": password
    }
    response = client.post(
        "/login",
        json=data
    )
    assert response.status_code == 200
    assert "Authorization" in response.cookies
    token_value = response.cookies["Authorization"]
    assert token_value is not None
    assert token_value.strip('"').startswith("Bearer")
    assert response.json()["first_name"] == admin.first_name
    assert response.json()["last_name"] == admin.last_name
    assert response.json()["email"] == admin.email
    assert response.json()["is_admin"] == admin.is_admin


async def test_login_handler_wrong_password(admin_user):
    admin, user_data, password = admin_user
    data = {
            "login": user_data["email"], "password": "wrong_password"
    }
    response = client.post(
        "/login",
        json=data
    )
    assert response.status_code == 400
    assert "Authorization" not in response.cookies
    assert response.json() == {
        'code': 400,
        'message': {
            'code': 400,
            'message': 'Incorrect email or password'
        }
    }


async def test_logout_handler(admin_user):
    admin, user_data, password = admin_user
    data = {
            "login": user_data["email"], "password": password
    }
    response = client.post(
        "/login",
        json=data
    )
    assert response.status_code == 200
    assert "Authorization" in response.cookies
    token_value = response.cookies["Authorization"]
    assert token_value is not None
    assert token_value.strip('"').startswith("Bearer")
    response = client.get(
        "/logout",
    )
    assert response.status_code == 200
    assert "Authorization" not in response.cookies
