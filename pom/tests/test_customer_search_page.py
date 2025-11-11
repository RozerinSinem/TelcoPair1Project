import pytest
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.customer_info_page import CustomerInfoPage
from pages.customer_search_page import CustomerSearchPage
from constants.credentials import VALID_USERNAME, VALID_PASSWORD
import time

class TestCustomerSearchPage:

     @pytest.fixture(autouse=True)
     def setup(self, driver, wait):
        self.login_page = LoginPage(driver, wait)
        self.customer_search_page = CustomerSearchPage(driver, wait)
        self.login_page.load()
        self.login_page.login(VALID_USERNAME, VALID_PASSWORD)

     def test_elements_visibility_order(self):
        fields = [
            self.customer_search_page.NATID_INPUT,
            self.customer_search_page.CUSTNUM_INPUT,
            self.customer_search_page.ACCNUM_INPUT,
            self.customer_search_page.GSM_INPUT,
            self.customer_search_page.FIRSTNAME_INPUT,
            self.customer_search_page.LASTNAME_INPUT,
            self.customer_search_page.ORDERNUM_INPUT
        ]
        for locator in fields:
            assert self.customer_search_page.utils.is_element_visible(locator), f"{locator} görünmüyor!"
     def test_mutual_exclusion_and_clear_flow(self):
        unique_fields = [
            self.customer_search_page.NATID_INPUT,
            self.customer_search_page.CUSTNUM_INPUT,
            self.customer_search_page.ACCNUM_INPUT,
            self.customer_search_page.GSM_INPUT,
            self.customer_search_page.ORDERNUM_INPUT
        ]

        test_values = {
            self.customer_search_page.NATID_INPUT: "12345678901",
            self.customer_search_page.CUSTNUM_INPUT: "1001",
            self.customer_search_page.ACCNUM_INPUT: "ACC123",
            self.customer_search_page.GSM_INPUT: "5551234567",
            self.customer_search_page.ORDERNUM_INPUT: "ORD456"
        }

        for active_field in unique_fields:
            # Clear butonuna basarak tüm alanları sıfırla
            self.customer_search_page.utils.click_element(self.customer_search_page.CLEAR_BUTTON)

            # Aktif alana veri gir
            self.customer_search_page.utils.fill_input_field(active_field, test_values[active_field])

            # Diğer alanların devre dışı olduğunu kontrol et
            for field in unique_fields:
                if field == active_field:
                    continue
                assert not self.customer_search_page.utils.is_button_enabled(field), f"{field} {active_field} girildiğinde devre dışı kalmalı!"

            # Clear butonuna tekrar bas
            self.customer_search_page.utils.click_element(self.customer_search_page.CLEAR_BUTTON)

            # Tüm alanların yeniden aktif olduğunu kontrol et
            for field in unique_fields:
                assert self.customer_search_page.utils.is_button_enabled(field), f"{field} clear sonrası aktif olmalı!"

     def test_partial_firstname_search(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.FIRSTNAME_INPUT, "Cer")
        self.customer_search_page.utils.click_element(self.customer_search_page.SEARCH_BUTTON)
        self.customer_search_page.utils.wait_for_element(("css selector", "#res-list > div"))
        rows = self.customer_search_page.driver.find_elements(By.CSS_SELECTOR, "#res-list > div")
        assert any("Cer" in row.text for row in rows), "İsim araması başarısız!"

     def test_partial_lastname_search(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.LASTNAME_INPUT, "Kay")
        self.customer_search_page.utils.click_element(self.customer_search_page.SEARCH_BUTTON)
        self.customer_search_page.utils.wait_for_element(("css selector", "#res-list > div"))
        rows = self.customer_search_page.driver.find_elements(By.CSS_SELECTOR, "#res-list > div")
        assert any("Kay" in row.text for row in rows), "Soyisim araması başarısız!"

     def test_combined_name_search(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.FIRSTNAME_INPUT, "Cer")
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.LASTNAME_INPUT, "Kay")
        self.customer_search_page.utils.click_element(self.customer_search_page.SEARCH_BUTTON)
        self.customer_search_page.utils.wait_for_element(("css selector", "#res-list > div"))
        rows = self.customer_search_page.driver.find_elements(By.CSS_SELECTOR, "#res-list > div")
        assert all("Cer" in row.text and "Kay" in row.text for row in rows), "İkili isim araması başarısız!"

     def test_search_button_default_state(self):
        assert not self.customer_search_page.utils.is_button_enabled(self.customer_search_page.SEARCH_BUTTON), "Arama butonu başlangıçta aktif olmamalı!"

     def test_search_button_activation(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.CUSTNUM_INPUT, "10001")
        assert self.customer_search_page.utils.is_button_enabled(self.customer_search_page.SEARCH_BUTTON), "Arama butonu aktifleşmedi!"

   

     def test_clear_button_resets_fields(self):
        # 1. Alanlara veri gir
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.CUSTNUM_INPUT, "10001")
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.FIRSTNAME_INPUT, "Ceren")
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.LASTNAME_INPUT, "Kay")

        # 2. Search butonunun aktif olduğunu doğrula
        assert self.customer_search_page.utils.is_button_enabled(self.customer_search_page.SEARCH_BUTTON), "Arama butonu veri girildikten sonra aktif olmalı!"

        # 3. Clear butonuna bas
        self.customer_search_page.utils.click_element(self.customer_search_page.CLEAR_BUTTON)

        # 4. Tüm alanların boş olduğunu kontrol et
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
            time.sleep(1)  # Alanların DOM'da güncellenmesini beklemek için
            value = self.customer_search_page.utils.get_input_value(field)
            assert value == "", f"{field} temizlenmedi!"

        # 5. Search butonunun yeniden pasif olduğunu doğrula
        assert not self.customer_search_page.utils.is_button_enabled(self.customer_search_page.SEARCH_BUTTON), "Arama butonu temizlemeden sonra pasif olmalı!"


     def test_search_result_table_display(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.FIRSTNAME_INPUT, "Ceren")
        self.customer_search_page.utils.click_element(self.customer_search_page.SEARCH_BUTTON)
        self.customer_search_page.utils.wait_for_element(("css selector", "#res-list > div"))
        rows = self.customer_search_page.driver.find_elements(By.CSS_SELECTOR, "#res-list > div")
        assert len(rows) > 0, "Arama sonucu görünmüyor!"

     def test_no_customer_found_alert(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.FIRSTNAME_INPUT, "x")
        self.customer_search_page.utils.click_element(self.customer_search_page.SEARCH_BUTTON)
        assert self.customer_search_page.utils.is_element_visible(self.customer_search_page.NO_CUSTOMER_ALERT), "Uyarı görünmüyor!"
        alert_text = self.customer_search_page.utils.get_element_text(self.customer_search_page.NO_CUSTOMER_ALERT)
        assert "No customer found!" in alert_text, "Beklenen uyarı metni yok!"

     def test_create_customer_button_visible_and_clickable(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.FIRSTNAME_INPUT, "x")
        self.customer_search_page.utils.click_element(self.customer_search_page.SEARCH_BUTTON)
        assert self.customer_search_page.utils.is_element_visible(self.customer_search_page.CREATE_CUSTOMER_BUTTON), "Müşteri oluştur butonu görünmüyor!"
        assert self.customer_search_page.utils.wait_for_element(self.customer_search_page.CREATE_CUSTOMER_BUTTON).is_enabled(), "Müşteri oluştur butonu tıklanabilir değil!"

     def test_click_customer_id_opens_customer_info(self):
        self.customer_search_page.utils.fill_input_field(self.customer_search_page.FIRSTNAME_INPUT, "Ceren")
        self.customer_search_page.utils.click_element(self.customer_search_page.SEARCH_BUTTON)
        self.customer_search_page.utils.scroll_into_view(self.customer_search_page.CUSTOMER_ID_BUTTON)
        self.customer_search_page.utils.click_element(self.customer_search_page.CUSTOMER_ID_BUTTON)
        customer_info_page = CustomerInfoPage(self.customer_search_page.driver, self.customer_search_page.wait)
        assert customer_info_page.utils.is_element_visible(customer_info_page.INFO_TAB), "Bilgi sekmesi görünmüyor!"
