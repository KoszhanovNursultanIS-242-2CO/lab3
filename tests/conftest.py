import os
import pytest
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from logger import get_logger

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
HUB_URL = os.getenv("HUB_URL", "http://localhost:4444/wd/hub")

@pytest.fixture(scope="session")
def logger():
    return get_logger("lab3")

@pytest.fixture(scope="session")
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Remote(
        command_executor=HUB_URL,
        options=options
    )
    yield driver
    driver.quit()

@pytest.fixture
def api_url():
    return BASE_URL + "/api/users"

@pytest.fixture(autouse=True)
def clean_db():
    # Очищаем таблицу перед каждым тестом, чтобы не было дубликатов email
    if os.path.exists("users.db"):
        try:
            conn = sqlite3.connect("users.db", timeout=10.0)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users")
            conn.commit()
            conn.close()
        except sqlite3.OperationalError:
            pass