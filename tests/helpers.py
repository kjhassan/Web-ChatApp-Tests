import json
import time
from datetime import datetime
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clear_session(driver, app_url):
    driver.get(app_url)

    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")


def wait_for_text(driver, locator, text, timeout=10):
    WebDriverWait(driver, timeout).until(
        EC.text_to_be_present_in_element(locator, text)
    )


def wait_for_element(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )


def wait_for_clickable(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )


def fill_signup_form(driver, user):
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="John Doe"]').send_keys(user["fullname"])
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="johndoe"]').send_keys(user["username"])
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter Password"]').send_keys(user["password"])
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Confirm Password"]').send_keys(user["confirmPassword"])
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="enter contact no"]').send_keys(user["contactno"])

    # Gender radio (your UI uses <label><span>Male</span></label>)
    gender_label = driver.find_element(By.XPATH, f"//label[.//span[text()='{user['gender'].capitalize()}']]")
    gender_label.click()


def login(driver, base_url, username, password):
    clear_session(driver, base_url)
    driver.get(f"{base_url}/login")

    wait_for_element(driver, (By.CSS_SELECTOR, 'input[placeholder="Enter username"]'))
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter username"]').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter Password"]').send_keys(password)

    # Login button (class: btn btn-block btn-sm mt-2)
    driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-block').click()

    WebDriverWait(driver, 10).until(lambda d: "/login" not in d.current_url)


def open_home(driver, base_url):
    driver.get(base_url)
    WebDriverWait(driver, 10).until(lambda d: "/login" not in d.current_url)


def ensure_conversation_selected(driver):
    cards = WebDriverWait(driver, 10).until(
        lambda d: d.find_elements(By.CSS_SELECTOR, "div.cursor-pointer")
    )
    if len(cards) == 0:
        pytest.skip("No conversations available to select for this user")

    cards[0].click()

    wait_for_text(driver, (By.CSS_SELECTOR, "div.bg-slate-500"), "To:")


def local_storage_chat_user(driver):
    raw = driver.execute_script("return window.localStorage.getItem('chat-user');")
    return json.loads(raw) if raw else None
