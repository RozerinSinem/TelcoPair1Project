from selenium.webdriver.common.by import By
from helpers.utils import Utils
from constants.urls import BASE_URL

class CustomerInfoPage:
    INFO_TAB = (By.ID, "tab-info-label")
    ACCOUNT_TAB = (By.ID, "tab-account-label")
    ADDRESS_TAB = (By.ID, "tab-address-label")
    CONTACT_TAB = (By.ID, "tab-contact-label")

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.utils = Utils(driver, wait)