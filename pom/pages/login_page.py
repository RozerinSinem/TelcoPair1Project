from selenium.webdriver.common.by import By
from helpers.utils import Utils
from constants.urls import BASE_URL




class LoginPage:
    USERNAME_INPUT = (By.ID, "login-email")
    PASSWORD_INPUT = (By.ID, "login-password")
    LOGIN_BUTTON = (By.XPATH, "//*[@type='submit']")
    EYE_ICON = (By.XPATH, "//*[@aria-label='Toggle password visibility']")
    LOGIN_ALERT = (By.ID,"login-global-error")

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.utils = Utils(driver, wait)

    def load(self):
        """Login sayfasını açar."""
        self.driver.get(BASE_URL)

    def login(self, username, password):
        """Kullanıcı adı ve şifre girip login butonuna tıklar."""
        self.utils.fill_input_field(self.USERNAME_INPUT, username)
        self.utils.fill_input_field(self.PASSWORD_INPUT, password)
        self.utils.click_element(self.LOGIN_BUTTON)
