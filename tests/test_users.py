from tests.conftest import client


async def test_get_users(
        authorized_admin_client
):
    cookies, admin, user_data, password = authorized_admin_client
    headers = {
        "Cookie": f"Authorization={cookies['Authorization']}"
    }
    response = client.get(
        f"/users/",
        headers=headers,
    )
    assert response.status_code == 200
    users_data = response.json()["data"]
    assert "data" in response.json()
    assert len(users_data) == 2
    assert "meta" in response.json()


async def test_get_current_user(
        authorized_user_client
):
    cookies, admin, user_data, password = authorized_user_client
    headers = {
        "Cookie": f"Authorization={cookies['Authorization']}"
    }
    response = client.get(
        f"/users/current",
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == user_data["first_name"]
    assert response.json()["last_name"] == user_data["last_name"]
    assert response.json()["email"] == user_data["email"]
    assert response.json()["is_admin"] == user_data["is_admin"]
    assert "password" not in response.json()


async def test_update_current_user(
        authorized_user_client
):
    cookies, admin, user_data, password = authorized_user_client
    headers = {
        "Cookie": f"Authorization={cookies['Authorization']}"
    }
    data = {
        "first_name": "new",
        "last_name": "new",
    }
    response = client.patch(
        f"/users/current",
        json=data,
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["id"] == admin.id
    assert response.json()["first_name"] == data["first_name"]
    assert response.json()["last_name"] == data["last_name"]
    assert response.json()["email"] == user_data["email"]
