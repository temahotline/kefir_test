from tests.conftest import client


async def test_private_users_handler_with_admin(
        authorized_admin_client):
    cookies, admin, user_data, password = authorized_admin_client
    headers = {
        "Cookie": f"Authorization={cookies['Authorization']}"
    }
    response = client.get("/private/users", headers=headers)
    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == admin.id
    assert response.json()["data"][0]["first_name"] == admin.first_name
    assert response.json()["data"][0]["last_name"] == admin.last_name
    assert response.json()["data"][0]["email"] == admin.email
    assert "meta" in response.json()
    assert "pagination" in response.json()["meta"]
    assert "total" in response.json()["meta"]["pagination"]
    assert "page" in response.json()["meta"]["pagination"]
    assert "size" in response.json()["meta"]["pagination"]
    assert "hint" in response.json()["meta"]
    assert "city" in response.json()["meta"]["hint"]


async def test_private_users_handler_with_user(
        authorized_user_client):
    cookies, user, user_data, password = authorized_user_client
    headers = {
        "Cookie": f"Authorization={cookies['Authorization']}"
    }
    response = client.get("/private/users", headers=headers)
    assert response.status_code == 403
    assert response.json() == {
        "message": "Доступ разрешен только администраторам"
    }


async def test_private_users_handler_without_auth():
    response = client.get("/private/users")
    assert response.status_code == 401
    assert response.json() == {
        "message": "Пользователь не опознан"
    }


async def test_private_create_user(
        authorized_admin_client
):
    cookies, admin, user_data, password = authorized_admin_client
    headers = {
        "Cookie": f"Authorization={cookies['Authorization']}"
    }
    data = {
        "first_name": "test",
        "last_name": "test",
        "email": "test@test.ru",
        "is_admin": False,
        "password": "test",
    }
    response = client.post(
        "/private/users",
        json=data,
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["first_name"] == data["first_name"]
    assert response.json()["last_name"] == data["last_name"]
    assert response.json()["email"] == data["email"]
    assert response.json()["is_admin"] == data["is_admin"]
    assert "id" in response.json()
    assert "password" not in response.json()


async def test_get_user_by_id(
        authorized_admin_client
):
    cookies, admin, user_data, password = authorized_admin_client
    headers = {
        "Cookie": f"Authorization={cookies['Authorization']}"
    }
    response = client.get(
        f"/private/users/{admin.id}",
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == admin.first_name
    assert response.json()["last_name"] == admin.last_name
    assert response.json()["email"] == admin.email
    assert response.json()["is_admin"] == admin.is_admin
    assert response.json()["id"] == admin.id
    assert "password" not in response.json()


async def test_update_user_by_id(
        authorized_admin_client
):
    cookies, admin, user_data, password = authorized_admin_client
    headers = {
        "Cookie": f"Authorization={cookies['Authorization']}"
    }
    data = {
        "id": admin.id,
        "first_name": "new",
        "last_name": "new",
    }
    response = client.patch(
        f"/private/users/{admin.id}",
        json=data,
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == data["first_name"]
    assert response.json()["last_name"] == data["last_name"]
    assert response.json()["email"] == admin.email
    assert response.json()["is_admin"] == admin.is_admin


async def test_delete_user_by_id(
        authorized_admin_client
):
    cookies, admin, user_data, password = authorized_admin_client
    headers = {
        "Cookie": f"Authorization={cookies['Authorization']}"
    }
    response = client.delete(
        f"/private/users/{admin.id}",
        headers=headers,
    )
    assert response.status_code == 204
