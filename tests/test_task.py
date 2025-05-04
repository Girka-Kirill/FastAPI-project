def test_create_task(client, test_user):
    login_response = client.post(
        "/token",
        data={"email": "test@example.com", "password": "testpass"}
    )
    token = login_response.json()["access_token"]
    
    task_data = {
        "title": "Test Task",
        "description": "Test Description"
    }
    
    response = client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["owner_id"] == test_user["id"]

def test_get_task(client, test_user):
    # Сначала создаем задачу
    login_response = client.post(
        "/token",
        data={"email": "test@example.com", "password": "testpass"}
    )
    token = login_response.json()["access_token"]
    
    create_response = client.post(
        "/tasks/",
        json={"title": "Test Task"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]
    
    # Теперь получаем задачу
    response = client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == task_id

def test_update_task(client, test_user):
    login_response = client.post(
        "/token",
        data={"email": "test@example.com", "password": "testpass"}
    )
    token = login_response.json()["access_token"]
    
    # Создаем задачу
    create_response = client.post(
        "/tasks/",
        json={"title": "Original Title"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]
    
    # Обновляем задачу
    update_response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated Title", "status": "completed"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Title"
    assert update_response.json()["status"] == "completed"

def test_delete_task(client, test_user):
    login_response = client.post(
        "/token",
        data={"email": "test@example.com", "password": "testpass"}
    )
    token = login_response.json()["access_token"]
    
    # Создаем задачу
    create_response = client.post(
        "/tasks/",
        json={"title": "Task to delete"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]
    
    # Удаляем задачу
    delete_response = client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_response.status_code == 200
    
    # Проверяем, что задача удалена
    get_response = client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 404