from selenium.webdriver.common.by import By

def test_sidebar_components(driver, base_url):
    driver.get(base_url + "/login")

    driver.find_element(By.XPATH, "//input[@placeholder='Enter username']").send_keys("testuser")
    driver.find_element(By.XPATH, "//input[@placeholder='Enter Password']").send_keys("password123")
    driver.find_element(By.XPATH, "//button[contains(@class,'btn-block')]").click()

    # Search bar exists
    search = driver.find_element(By.XPATH, "//input[contains(@placeholder,'Search')]")
    assert search is not None
