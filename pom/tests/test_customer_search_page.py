import pytest
from pages.login_page import LoginPage
from pages.customer_info_page import CustomerInfoPage
from pages.customer_search_page import CustomerSearchPage
from constants.credentials import VALID_USERNAME, VALID_PASSWORD

class TestCustomerSearchPage:

    @pytest.fixture(autouse=True)
    def setup(self, driver, wait):
        self.login_page = LoginPage(driver, wait)
        self.customer_search_page = CustomerSearchPage(driver, wait)
        self.login_page.load()
        self.login_page.login(VALID_USERNAME, VALID_PASSWORD)

    def test_elements_visibility_order(self):
        fields = [
            (self.customer_search_page.NATID_INPUT, "NAT ID Number input görünmüyor!"),
            (self.customer_search_page.CUSTNUM_INPUT, "Customer ID input görünmüyor!"),
            (self.customer_search_page.ACCNUM_INPUT, "Account Number input görünmüyor!"),
            (self.customer_search_page.GSM_INPUT, "GSM input görünmüyor!"),
            (self.customer_search_page.FIRSTNAME_INPUT, "First Name input görünmüyor!"),
            (self.customer_search_page.LASTNAME_INPUT, "Last Name input görünmüyor!"),
            (self.customer_search_page.ORDERNUM_INPUT, "Order Number input görünmüyor!")
        ]
        for locator, msg in fields:
            assert self.customer_search_page.utils.is_element_visible(locator), msg

    def test_unique_id_fields_mutual_exclusion(self):
        unique_fields = [
            self.customer_search_page.NATID_INPUT,
            self.customer_search_page.CUSTNUM_INPUT,
            self.customer_search_page.ACCNUM_INPUT,
            self.customer_search_page.GSM_INPUT,
            self.customer_search_page.ORDERNUM_INPUT
        ]

        for active_field in unique_fields:
            for field in unique_fields:
                self.customer_search_page.utils.fill_input_field(field, "")
            self.customer_search_page.utils.fill_input_field(active_field, "1001")

            for field in unique_fields:
                if field == active_field:
                    continue
                assert not self.customer_search_page.utils.is_element_visible(field) or not self.customer_search_page.utils.is_button_enabled(field), \
                    f"{field} should be disabled when {active_field} is filled"

    def test_fields_reenabled_after_deletion(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.CUSTNUM_INPUT, "1001")
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.CUSTNUM_INPUT, "")
        other_unique_fields = [
            self.customer_search_page.NATID_INPUT,
            self.customer_search_page.ACCNUM_INPUT,
            self.customer_search_page.GSM_INPUT,
            self.customer_search_page.ORDERNUM_INPUT
        ]
        for field in other_unique_fields:
            assert self.customer_search_page.utils.is_element_visible(field) and self.customer_search_page.utils.is_button_enabled(field), f"{field} should be re-enabled!"

    def test_partial_firstname_search(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.FIRSTNAME_INPUT, "Cer")
        self.customer_search_page.utils.click_element(self.customer_search_page.SEARCH_BUTTON)
        rows = self.customer_search_page.driver.find_elements_by_css_selector("table tbody tr")
        assert any("Cer" in row.text for row in rows), "Partial first name search failed"

    def test_partial_lastname_search(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.LASTNAME_INPUT, "Kay")
        self.customer_search_page.utils.click_element(self.customer_search_page.SEARCH_BUTTON)
        rows = self.customer_search_page.driver.find_elements_by_css_selector("table tbody tr")
        assert any("Kay" in row.text for row in rows), "Partial last name search failed"

    def test_combined_name_search(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.FIRSTNAME_INPUT, "Cer")
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.LASTNAME_INPUT, "Kay")
        self.customer_search_page.utils.click_element(self.customer_search_page.SEARCH_BUTTON)
        rows = self.customer_search_page.driver.find_elements_by_css_selector("table tbody tr")
        assert all("Cer" in row.text and "Kay" in row.text for row in rows), "Combined name search failed"

    def test_search_button_default_state(self):
        assert not self.customer_search_page.utils.is_button_enabled(self.customer_search_page.SEARCH_BUTTON), "Search button should be disabled initially"

    def test_search_button_activation(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.CUSTNUM_INPUT, "10001")
        assert self.customer_search_page.utils.is_button_enabled(self.customer_search_page.SEARCH_BUTTON), "Search button did not activate"

    def test_clear_button_resets_fields(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.CUSTNUM_INPUT, "10001")
        self.customer_search_page.utils.click_element(self.customer_search_page.CLEAR_BUTTON)
        fields = [
            self.customer_search_page.NATID_INPUT,
            self.customer_search_page.CUSTNUM_INPUT,
            self.customer_search_page.ACCNUM_INPUT,
            self.customer_search_page.GSM_INPUT,
            self.customer_search_page.ORDERNUM_INPUT,
            self.customer_search_page.FIRSTNAME_INPUT,
            self.customer_search_page.LASTNAME_INPUT
        ]
        for field in fields:
            value = self.customer_search_page.utils.get_element_text(field)
            assert value == "", f"{field} not cleared"
        assert not self.customer_search_page.utils.is_button_enabled(self.customer_search_page.SEARCH_BUTTON), "Search button should be disabled after clear"

    def test_search_result_table_display(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.FIRSTNAME_INPUT, "Ceren")
        self.customer_search_page.utils.click_element(self.customer_search_page.SEARCH_BUTTON)
        rows = self.customer_search_page.driver.find_elements_by_css_selector("")
        assert len(rows) > 0, "No search results displayed"

    def test_no_customer_found_alert(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.FIRSTNAME_INPUT, "x")
        self.customer_search_page.utils.click_element(self.customer_search_page.SEARCH_BUTTON)
        assert self.customer_search_page.utils.is_element_visible(self.customer_search_page.NO_CUSTOMER_ALERT), "No-customer-found alert is not visible!"
        alert_text = self.customer_search_page.utils.get_element_text(self.customer_search_page.NO_CUSTOMER_ALERT)
        expected_text = "No customer found! Would you like to create a customer?"
        assert expected_text in alert_text, f"Expected alert text not found! Actual: {alert_text}"

    def test_create_customer_button_visible_and_clickable(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.FIRSTNAME_INPUT, "x")
        self.customer_search_page.utils.click_element(self.customer_search_page.SEARCH_BUTTON)
        assert self.customer_search_page.utils.is_element_visible(self.customer_search_page.CREATE_CUSTOMER_BUTTON), "'Müşteri Oluştur' button not visible when no record found!"
        assert self.customer_search_page.utils.wait_for_element(self.customer_search_page.CREATE_CUSTOMER_BUTTON).is_enabled(), "'Müşteri Oluştur' button is not clickable!"

    def test_click_customer_id_opens_customer_info(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.FIRSTNAME_INPUT, "Ceren")
        self.customer_search_page.utils.click_element(self.customer_search_page.SEARCH_BUTTON)
        self.customer_search_page.utils.click_element(self.customer_search_page.CUSTOMER_ID_BUTTON)
        customer_info_page = CustomerInfoPage(self.customer_search_page.driver, self.customer_search_page.wait)
        assert customer_info_page.utils.is_element_visible(customer_info_page.INFO_TAB), "Customer Info tab is not visible after clicking Customer ID!"
