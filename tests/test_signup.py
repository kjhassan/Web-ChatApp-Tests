from selenium.webdriver.common.by import By

def test_signup_page_load(driver, base_url):
    driver.get(base_url + "/signup")
    assert "Signup" in driver.page_source


def test_signup_success(driver, base_url):
    driver.get(base_url + "/signup")

    driver.find_element(By.XPATH, "//input[@placeholder='johndoe']").send_keys("user123")
    driver.find_element(By.XPATH, "//input[@placeholder='Enter Password']").send_keys("password123")

    # confirm password field = second password input
    confirm = driver.find_elements(By.XPATH, "//input[@placeholder='Enter Password']")[1]
    confirm.send_keys("password123")

    register_btn = driver.find_element(By.XPATH, "//button[contains(@class,'btn-block')]")
    register_btn.click()

    assert "/login" in driver.current_url
