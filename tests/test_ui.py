from selenium.webdriver.common.by import By
import time

BASE_URL = "http://web:5000"

def test_ui_register_user(driver, logger):
    logger.info("UI: регистрация пользователя")
    driver.get(BASE_URL + "/register")
    driver.find_element(By.NAME, "name").send_keys("Ivan")
    driver.find_element(By.NAME, "email").send_keys("ivan@test.com")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    assert "Ivan (ivan@test.com)" in driver.page_source