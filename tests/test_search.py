from helpers import *
import time


def test_search_requires_min_length_and_selects_match(driver, app_url, test_users):
    user = test_users["user_a"]
    login(driver, app_url, user["username"], user["password"])

    # Correct real placeholder: Search… (Unicode ellipsis)
    search_input = wait_for_element(driver, (By.CSS_SELECTOR, 'input[placeholder="Search…"]'))

    search_input.clear()
    search_input.send_keys("ab")

    driver.find_element(By.CSS_SELECTOR, "button.btn.btn-circle[type='submit']").click()

    # Too short → no conversation selected
    assert "To:" not in driver.page_source

    # Now search valid prefix
    search_input.clear()
    search_input.send_keys(user["fullname"].split()[0][:3].lower())
    driver.find_element(By.CSS_SELECTOR, "button.btn.btn-circle[type='submit']").click()

    WebDriverWait(driver, 5).until(lambda d: "To:" in d.page_source)
