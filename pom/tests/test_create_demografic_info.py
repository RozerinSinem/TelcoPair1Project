from selenium.webdriver.common.by import By
import pytest

class TestCreateDemograficInfoPage:
    validation_message_selector = ".text-sm.text-red-600.mt-1"
    validation_text = "Only letters (2–50 chars)" 

    @pytest.fixture(autouse=True)
    def setup(self, driver, wait):
        """Login and navigate to Demographic Info screen."""
        from pages.login_page import LoginPage
        from pages.customer_search_page import CustomerSearchPage
        from constants.credentials import VALID_USERNAME, VALID_PASSWORD
        from pages.create_demografic_info import CreateDemograficInfoPage

        self.login_page = LoginPage(driver, wait)
        self.customer_search_page = CustomerSearchPage(driver, wait)
        self.login_page.load()
        self.login_page.login(VALID_USERNAME, VALID_PASSWORD)
        self.customer_search_page.utils.fill_input_field(
            self.customer_search_page.FIRSTNAME_INPUT, "x"
        )
        self.customer_search_page.utils.click_element(
            self.customer_search_page.SEARCH_BUTTON
        )
        self.customer_search_page.utils.click_element(
            self.customer_search_page.CREATE_CUSTOMER_BUTTON
        )
        self.create_demografic_info = CreateDemograficInfoPage(driver, wait)

    def check_input_validation(self, input_field, short_value, digit_value, field_name):
        """Helper function to check letter-only and length validation for a field."""
        # Tek harf -> validation olmalı
        self.create_demografic_info.utils.fill_input_field(input_field, short_value)
        messages = self.create_demografic_info.utils.driver.find_elements(
            By.CSS_SELECTOR, self.validation_message_selector
        )
        message_texts = [msg.text for msg in messages if msg.is_displayed()]
        assert any(self.validation_text in text for text in message_texts), \
            f"Validation message should appear for {field_name} < 2 chars"

        # Sayı -> validation olmalı
        self.create_demografic_info.utils.fill_input_field(input_field, digit_value)
        messages = self.create_demografic_info.utils.driver.find_elements(
            By.CSS_SELECTOR, self.validation_message_selector
        )
        message_texts = [msg.text for msg in messages if msg.is_displayed()]
        assert any(self.validation_text in text for text in message_texts), \
            f"Validation message should appear for {field_name} containing digit"

    def test_first_name_letter_only_and_length(self):
        self.check_input_validation(
            self.create_demografic_info.CREATE_FIRST_NAME,
            short_value="m",
            digit_value="M3",
            field_name="First Name"
        )

    def test_middle_name_letter_only_and_length(self):
        self.check_input_validation(
            self.create_demografic_info.CREATE_MIDDLE_NAME,
            short_value="m",
            digit_value="A7",
            field_name="Middle Name"
        )

    def test_last_name_letter_only_and_length(self):
        self.check_input_validation(
            self.create_demografic_info.CREATE_LAST_NAME,
            short_value="m",
            digit_value="Art1",
            field_name="Last Name"
        )

    def test_father_name_letter_only_and_length(self):
        self.check_input_validation(
            self.create_demografic_info.CREATE_FATHER_NAME,
            short_value="m",
            digit_value="F4",
            field_name="Father Name"
        )

    def test_mother_name_letter_only_and_length(self):
        self.check_input_validation(
            self.create_demografic_info.CREATE_MOTHER_NAME,
            short_value="m",
            digit_value="M5",
            field_name="Mother Name"
        )
