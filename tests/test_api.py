import requests

def test_api_create_user(api_url, logger):
    logger.info("Создание пользователя через API")
    payload = {"name": "Ivan", "email": "ivan@test.com"}
    response = requests.post(api_url, json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Ivan"
    assert data["email"] == "ivan@test.com"

def test_api_get_users(api_url, logger):
    logger.info("Получение списка пользователей через API")
    response = requests.get(api_url)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_api_create_duplicate_user(api_url, logger):
    logger.info("Создание пользователя с дублирующим email")
    payload = {"name": "Ivan", "email": "ivan@test.com"}
    requests.post(api_url, json=payload)
    response2 = requests.post(api_url, json=payload)
    assert response2.status_code in [400, 500]

def test_api_delete_user(api_url, logger):
    logger.info("Удаление пользователя через API")
    payload = {"name": "Alex", "email": "alex@test.com"}
    response = requests.post(api_url, json=payload)
    user_id = response.json()["id"]
    del_resp = requests.delete(f"{api_url}/{user_id}")
    assert del_resp.status_code == 204