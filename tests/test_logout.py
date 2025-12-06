from helpers import *


def test_logout_clears_session(driver, app_url, test_users):
    user = test_users["user_a"]
    login(driver, app_url, user["username"], user["password"])

    logout_icon = wait_for_clickable(
        driver,
        (By.CSS_SELECTOR, "svg.w-6.h-6.text-white.cursor-pointer")
    )
    logout_icon.click()

    WebDriverWait(driver, 10).until(lambda d: "/login" in d.current_url)

    assert local_storage_chat_user(driver) is None
