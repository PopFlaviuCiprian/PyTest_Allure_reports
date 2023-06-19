import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import allure

@pytest.fixture()
def test_setup():
    global driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield
    driver.quit()

@allure.description("Validates OrangeHRM with valid login credentials")
@allure.severity(severity_level='CRITICAL')
def test_valid_login(test_setup):
    driver.get('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')
    driver.find_element(By.NAME, 'username').clear()
    enter_username('Admin')
    driver.find_element(By.NAME, 'password').clear()
    enter_password('admin123')

    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    assert 'dashboard' in driver.current_url

@allure.description("Validates OrangeHRM with invalid login credentials")
@allure.severity("NORMAL")
def test_invalid_login(test_setup):
    driver.get('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')
    driver.find_element(By.NAME, 'username').clear()
    enter_username('admino')
    driver.find_element(By.NAME, 'password').clear()
    enter_password('admin123')
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    try:
        assert 'dashboard' in driver.current_url
    finally:
        if(AssertionError):
            allure.attach(driver.get_screenshot_as_png(),
                          name="invalid Credentials", attachment_type=allure.attachment_type.PNG)


@allure.step("Entering username as {0}")
def enter_username(username):
    driver.find_element(By.NAME, 'username').send_keys(username)


@allure.step("Entering password as {0}")
def enter_password(password):
    driver.find_element(By.NAME, "password").send_keys(password)


def test_teardown():
    driver.quit()
