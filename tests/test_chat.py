from helpers import *
from datetime import datetime


def test_conversation_list_and_selection(driver, app_url, test_users):
    user = test_users["user_a"]
    login(driver, app_url, user["username"], user["password"])

    ensure_conversation_selected(driver)

    header = driver.find_element(By.CSS_SELECTOR, "div.bg-slate-500")
    assert "To:" in header.text


def test_send_message_appends_bubble(driver, app_url, test_users):
    user = test_users["user_a"]
    login(driver, app_url, user["username"], user["password"])

    ensure_conversation_selected(driver)

    payload = f"selenium message {datetime.utcnow().isoformat()}"

    input_box = wait_for_element(driver, (By.CSS_SELECTOR, 'input[placeholder="Send a message"]'))
    input_box.clear()
    input_box.send_keys(payload)

    driver.find_element(By.CSS_SELECTOR, "form button").click()

    WebDriverWait(driver, 10).until(
        lambda d: any(payload in el.text for el in d.find_elements(By.CSS_SELECTOR, ".chat-bubble"))
    )
