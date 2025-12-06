from selenium.webdriver.common.by import By

def test_ui_elements_exist(driver, base_url):
    driver.get(base_url + "/login")

    driver.find_element(By.XPATH, "//input[@placeholder='Enter username']")
    driver.find_element(By.XPATH, "//input[@placeholder='Enter Password']")
    driver.find_element(By.XPATH, "//button[contains(@class,'btn-block')]")

    assert True
