def test_optimal_task_assignment(client, test_user, db):
    login_response = client.post(
        "/token",
        data={"email": "test@example.com", "password": "testpass"}
    )
    token = login_response.json()["access_token"]
    
    # Создаем несколько задач
    task1 = client.post(
        "/tasks/",
        json={"title": "Task 1", "priority": 3},
        headers={"Authorization": f"Bearer {token}"}
    ).json()
    
    task2 = client.post(
        "/tasks/",
        json={"title": "Task 2", "priority": 1},
        headers={"Authorization": f"Bearer {token}"}
    ).json()
    
    # Тестируем оптимальное назначение
    response = client.post(
        "/tasks/assign/optimal",
        json={"task_ids": [task1["id"], task2["id"]]},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assignments = response.json()
    assert len(assignments) == 2
    assert all(a["user_id"] == test_user["id"] for a in assignments)