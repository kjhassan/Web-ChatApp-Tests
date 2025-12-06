def test_navigation(driver, base_url):
    driver.get(base_url + "/login")
    assert "/login" in driver.current_url

    driver.get(base_url + "/signup")
    assert "/signup" in driver.current_url
