# config_test.py

import os
import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait

# 📁 "screenshots" klasörünü oluştur
os.makedirs("screenshots", exist_ok=True)


@pytest.fixture
def driver():
    driver = Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def wait(driver):
    yield WebDriverWait(driver, 10)


# 📸 Test hatasında ekran görüntüsü al
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_path = f"screenshots/{item.name}.png"
            driver.save_screenshot(screenshot_path)
            print(f"\n Screenshot saved to: {screenshot_path}")
