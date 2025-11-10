from selenium.webdriver.common.by import By
from helpers.utils import Utils
from constants.urls import BASE_URL



class CustomerSearchPage:
    """Customer Search Page — login sonrası erişilen ekran."""

    # Locators
    SEARCH_BUTTON = (By.XPATH, "//button[@type='button' and normalize-space(text())='Search']")

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.utils = Utils(driver, wait)

    def load(self):
        """Sayfayı açar (login sayfasından başlanır)."""
        self.driver.get(BASE_URL)

    
