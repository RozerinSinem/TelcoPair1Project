from selenium.webdriver.common.by import By
from helpers.utils import Utils
from constants.urls import BASE_URL

class CreateDemograficInfoPage:
    CREATE_FIRST_NAME = (By.ID, "di-firstname-input")
    CREATE_LAST_NAME = (By.ID, "di-lastname-input")
    CREATE_MOTHER_NAME = (By.ID, "di-mothername-input")
    CREATE_MIDDLE_NAME = (By.ID, "di-middlename-input")
    CREATE_FATHER_NAME = (By.ID, "di-fathername-input")
    CREATE_BIRTHDATE = (By.ID, "di-birthdate-input")
    SELECT_GENDER = (By.ID, "di-gender-select")
    CREATE_NATID = (By.ID, "di-nationalid-input")
    CANCEL_BUTTON = (By.ID, "di-cancel-btn")
    NEXT_BUTTON = (By.ID, "di-submit-btn")
    CONTINUE_EDITING_BUTTON = (By.ID, "di-cancel-continue-btn")
    CANCEL_CONFIRM_BUTTON = (By.ID, "di-cancel-confirm-btn")
    PAGE_TITLE = (By.ID, "di-title")
    VALIDATION_MESSAGES = (By.ID, "di-cancel-modal-title")
    validation_message_selector = ".text-sm.text-red-600.mt-1"
    validation_text = "Only letters (2–50 chars)" 




    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.utils = Utils(driver, wait)
    
    def fill_demographic_info(self, first_name, middle_name, last_name,
                          father_name, mother_name, birth_date, gender, national_id):
        """Fill all available demographic fields"""
        self.utils.fill_input_field(self.CREATE_FIRST_NAME, first_name)
        self.utils.fill_input_field(self.CREATE_MIDDLE_NAME, middle_name)
        self.utils.fill_input_field(self.CREATE_LAST_NAME, last_name)
        self.utils.fill_input_field(self.CREATE_FATHER_NAME, father_name)
        self.utils.fill_input_field(self.CREATE_MOTHER_NAME, mother_name)
        self.utils.fill_input_field(self.CREATE_BIRTHDATE, birth_date)
        self.utils.fill_input_field(self.CREATE_NATID, national_id)

        # Gender dropdown seçimi
        self.utils.click_element(self.SELECT_GENDER)
        gender_option = (By.XPATH, f"//option[contains(text(), '{gender}')]")
        self.utils.click_element(gender_option)

        # Dropdown kapansın diye başka bir alana odaklan
        self.utils.click_element(self.CREATE_LAST_NAME)

    def check_input_validation(self, input_field, short_value, digit_value, field_name):
        """Helper function to check letter-only and length validation for a field."""
        # Tek harf -> validation olmalı
        self.utils.fill_input_field(input_field, short_value)
        messages = self.utils.driver.find_elements(
            By.CSS_SELECTOR, self.validation_message_selector
        )
        message_texts = [msg.text for msg in messages if msg.is_displayed()]
        assert any(self.validation_text in text for text in message_texts), \
            f"Validation message should appear for {field_name} < 2 chars"

        # Sayı -> validation olmalı
        self.utils.fill_input_field(input_field, digit_value)
        messages = self.utils.driver.find_elements(
            By.CSS_SELECTOR, self.validation_message_selector
        )
        message_texts = [msg.text for msg in messages if msg.is_displayed()]
        assert any(self.validation_text in text for text in message_texts), \
            f"Validation message should appear for {field_name} containing digit"



    