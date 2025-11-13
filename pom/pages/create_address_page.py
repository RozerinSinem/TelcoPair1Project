from selenium.webdriver.common.by import By
from helpers.utils import Utils
from constants.urls import BASE_URL

class CreateAddressPage:

    CREATE_ADDRESS_BUTTON = (By.ID,"add-new-address-btn-empty")







    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.utils = Utils(driver, wait)