import sqlite3
import requests
import time

BASE_URL = "http://web:5000"

def test_integration_api_ui_db(driver, api_url, logger):
    logger.info("Интеграционный тест: API -> DB -> UI")
    payload = {"name": "Alex", "email": "alex@test.com"}
    resp = requests.post(api_url, json=payload)
    assert resp.status_code == 201
    user_id = resp.json()["id"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    assert user == ("Alex", "alex@test.com")

    driver.get(BASE_URL)
    time.sleep(1)
    assert "Alex (alex@test.com)" in driver.page_source