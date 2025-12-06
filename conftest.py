import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Base URL used by ALL tests
@pytest.fixture(scope="session")
def app_url():
    return "http://localhost:5000"   # Change to EC2 URL when testing on EC2


# Selenium WebDriver fixture
@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless=new")      # headless chrome
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    yield driver
    driver.quit()


# Test users used for login tests (matches your backend/database)
@pytest.fixture(scope="session")
def test_users():
    return {
        "user_a": {
            "username": "amama123",   # UPDATE based on your DB
            "password": "12345678",
            "fullname": "Amama Fatima"
        },
        "user_b": {
            "username": "hajra4",
            "password": "12345678",
            "fullname": "hajra"
        }
    }
