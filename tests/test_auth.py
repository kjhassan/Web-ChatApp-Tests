from helpers import *
import time


def test_redirects_to_login_when_unauthenticated(driver, app_url):
    clear_session(driver, app_url=app_url)
    driver.get(app_url)
    WebDriverWait(driver, 10).until(lambda d: "/login" in d.current_url)
    assert "Login" in driver.page_source


def test_signup_requires_fields(driver, app_url):
    clear_session(driver,app_url=app_url)
    driver.get(f"{app_url}/signup")

    wait_for_clickable(driver, (By.CSS_SELECTOR, 'button.btn.btn-block')).click()

    assert "/signup" in driver.current_url
    assert local_storage_chat_user(driver) is None


def test_password_mismatch_validation(driver, app_url):
    clear_session(driver, app_url)
    driver.get(f"{app_url}/signup")

    user = {
        "fullname": "Mismatch User",
        "username": f"mismatch_{int(time.time())}",
        "password": "Password123!",
        "confirmPassword": "Password123!!",
        "gender": "male",
        "contactno": str(int(time.time()))[-10:],
    }

    fill_signup_form(driver, user)
    driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-block').click()

    assert "/signup" in driver.current_url
    assert local_storage_chat_user(driver) is None


def test_successful_signup_creates_session(driver, app_url):
    clear_session(driver, app_url)
    driver.get(f"{app_url}/signup")

    unique_suffix = int(time.time() * 1000)

    user = {
        "fullname": f"Selenium {unique_suffix}",
        "username": f"selenium_{unique_suffix}",
        "password": "Password123!",
        "confirmPassword": "Password123!",
        "gender": "female",
        "contactno": f"9{unique_suffix}"[:10],
    }

    fill_signup_form(driver, user)
    driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-block').click()

    WebDriverWait(driver, 10).until(lambda d: "/login" not in d.current_url)

    assert local_storage_chat_user(driver) is not None


def test_invalid_login_fails(driver, app_url, test_users):
    user = test_users["user_a"]
    clear_session(driver, app_url=app_url)
    driver.get(f"{app_url}/login")

    wait_for_element(driver, (By.CSS_SELECTOR, 'input[placeholder="Enter username"]'))

    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter username"]').send_keys(user["username"])
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter Password"]').send_keys("WRONG PASSWORD")
    driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-block').click()

    WebDriverWait(driver, 10).until(lambda d: "/login" in d.current_url)

    assert local_storage_chat_user(driver) is None


def test_successful_login_redirects_home(driver, app_url, test_users):
    user = test_users["user_a"]
    login(driver, app_url, user["username"], user["password"])

    assert "/login" not in driver.current_url
    assert local_storage_chat_user(driver) is not None
