from selenium.webdriver.common.by import By
from helpers.utils import Utils
from constants.urls import BASE_URL



class CustomerSearchPage:
    """Customer Search Page — login sonrası erişilen ekran."""

    FIRSTNAME_INPUT = (By.ID, "srch-firstname-input")
    LASTNAME_INPUT = (By.ID, "srch-lastname-input")
    NATID_INPUT = (By.ID, "srch-natid-input")
    CUSTNUM_INPUT = (By.ID, "srch-custnum-input")
    ACCNUM_INPUT = (By.ID, "srch-accnum-input")
    GSM_INPUT = (By.ID, "srch-gsm-input")
    ORDERNUM_INPUT = (By.ID, "srch-ordernum-input")
    CLEAR_BUTTON = (By.ID, "srch-clear-btn")
    SEARCH_BUTTON = (By.ID, "srch-submit-btn")
    NO_CUSTOMER_ALERT = (By.ID,"res-empty-text")
    CREATE_CUSTOMER_BUTTON = (By.ID, "res-create-btn")
    CUSTOMER_ID_BUTTON = (By.ID,"res-custid-btn-c86c04cc-377f-4adf-b20a-84fa97161395")

 

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.utils = Utils(driver, wait)

    def load(self):
        """Sayfayı açar (login sayfasından başlanır)."""
        self.driver.get(BASE_URL)
    
    
