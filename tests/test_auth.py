def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "testpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_login(client, test_user):
    # Правильный формат для OAuth2
    response = client.post(
        "/token",
        data={
            "email": "test@example.com",
            "password": "testpass",
            "grant_type": "password",
            "scope": ""
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_current_user(client, test_user):
    # Сначала получаем токен
    login = client.post(
        "/token",
        data={
            "email": "test@example.com",
            "password": "testpass",
            "grant_type": "password",
            "scope": ""
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    token = login.json()["access_token"]
    
    # Теперь запрашиваем данные пользователя
    response = client.get(
        "/users/me/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.json()["email"] == "test@example.com"