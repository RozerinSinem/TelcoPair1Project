from selenium.webdriver.common.by import By
import pytest
from datetime import datetime, timedelta
from pages.create_address_page import CreateAddressPage

class TestCreateDemograficInfoPage:


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

 

    def test_first_name_letter_only_and_length(self):
        self.create_demografic_info.check_input_validation(
            self.create_demografic_info.CREATE_FIRST_NAME,
            short_value="m",
            digit_value="M3",
            field_name="First Name"
        )

    def test_middle_name_letter_only_and_length(self):
        self.create_demografic_info.check_input_validation(
            self.create_demografic_info.CREATE_MIDDLE_NAME,
            short_value="m",
            digit_value="A7",
            field_name="Middle Name"
        )

    def test_last_name_letter_only_and_length(self):
        self.create_demografic_info.check_input_validation(
            self.create_demografic_info.CREATE_LAST_NAME,
            short_value="m",
            digit_value="Art1",
            field_name="Last Name"
        )

    def test_father_name_letter_only_and_length(self):
        self.create_demografic_info.check_input_validation(
            self.create_demografic_info.CREATE_FATHER_NAME,
            short_value="m",
            digit_value="F4",
            field_name="Father Name"
        )

    def test_mother_name_letter_only_and_length(self):
        self.create_demografic_info.check_input_validation(
            self.create_demografic_info.CREATE_MOTHER_NAME,
            short_value="m",
            digit_value="M5",
            field_name="Mother Name"
        )
    def test_nat_id_must_end_with_even_number(self):
        """11111111111 girildiğinde 'Must end with an even number' uyarısı doğrulanmalı."""
        nat_id_input = self.create_demografic_info.CREATE_NATID
        self.create_demografic_info.utils.fill_input_field(nat_id_input, "11111111111")

        error_element = self.create_demografic_info.utils.driver.find_element(By.ID, "di-nationalid-err-even")
        assert error_element.is_displayed(), "Even number validation message should be visible"
        assert error_element.text == "Must end with an even number", "Validation text mismatch for even number check"
    def test_nat_id_must_be_11_digits(self):
        """11111 girildiğinde 'Must be 11 digits' uyarısı doğrulanmalı."""
        nat_id_input = self.create_demografic_info.CREATE_NATID
        self.create_demografic_info.utils.fill_input_field(nat_id_input, "11111")

        error_element = self.create_demografic_info.utils.driver.find_element(By.ID, "di-nationalid-err-format")
        assert error_element.is_displayed(), "11-digit format validation message should be visible"
        assert error_element.text == "Must be 11 digits", "Validation text mismatch for digit length check"
    def test_nat_id_cannot_start_with_zero(self):
        """01111111111 girildiğinde 'Cannot start with 0' uyarısı doğrulanmalı."""
        nat_id_input = self.create_demografic_info.CREATE_NATID
        self.create_demografic_info.utils.fill_input_field(nat_id_input, "01111111111")

        error_element = self.create_demografic_info.utils.driver.find_element(By.ID, "di-nationalid-err-start")
        assert error_element.is_displayed(), "Start-with-zero validation message should be visible"
        assert error_element.text == "Cannot start with 0", "Validation text mismatch for start-with-zero check"
    
    def test_gender_dropdown_options_are_visible(self):
        """Gender dropdown açıldığında 'Male', 'Female', 'Other' seçenekleri görünmeli."""
        gender_dropdown = self.create_demografic_info.SELECT_GENDER
        self.create_demografic_info.utils.click_element(gender_dropdown)

        # Option ID'lerine göre locate et
        male_option = self.create_demografic_info.utils.driver.find_element(By.ID, "di-gender-opt-male")
        female_option = self.create_demografic_info.utils.driver.find_element(By.ID, "di-gender-opt-female")
        other_option = self.create_demografic_info.utils.driver.find_element(By.ID, "di-gender-opt-other")

        # Görünürlük kontrolleri
        assert male_option.is_displayed(), "'Male' seçeneği görünür olmalı"
        assert female_option.is_displayed(), "'Female' seçeneği görünür olmalı"
        assert other_option.is_displayed(), "'Other' seçeneği görünür olmalı"
    def test_next_button_disabled_when_first_name_is_empty(self):
        """First Name boş bırakıldığında Next butonu aktif olmamalı."""
        self.create_demografic_info.fill_demographic_info(
            first_name="",  # Boş bırakılıyor
            middle_name="Ali",
            last_name="Yılmaz",
            father_name="Mehmet",
            mother_name="Ayşe",
            birth_date="01/01/1990",
            gender="Male",
            national_id="12345678912"
        )

        is_enabled = self.create_demografic_info.utils.is_button_enabled(self.create_demografic_info.NEXT_BUTTON)
        assert not is_enabled, "Next butonu First Name boşken aktif olmamalı"
    def test_next_button_disabled_when_last_name_is_empty(self):
        """Last Name boş bırakıldığında Next butonu aktif olmamalı."""
        self.create_demografic_info.fill_demographic_info(
            first_name="Ahmet",
            middle_name="Ali",
            last_name="",  # Boş bırakılıyor
            father_name="Mehmet",
            mother_name="Ayşe",
            birth_date="01/01/1990",
            gender="Male",
            national_id="12345678912"
        )

        is_enabled = self.create_demografic_info.utils.is_button_enabled(self.create_demografic_info.NEXT_BUTTON)
        assert not is_enabled, "Next butonu Last Name boşken aktif olmamalı"
    def test_next_button_disabled_when_birth_date_is_empty(self):
        """Birth Date boş bırakıldığında Next butonu aktif olmamalı."""
        self.create_demografic_info.fill_demographic_info(
            first_name="Ahmet",
            middle_name="Ali",
            last_name="Yılmaz",
            father_name="Mehmet",
            mother_name="Ayşe",
            birth_date="",  # Boş bırakılıyor
            gender="Male",
            national_id="12345678912"
        )

        is_enabled = self.create_demografic_info.utils.is_button_enabled(self.create_demografic_info.NEXT_BUTTON)
        assert not is_enabled, "Next butonu Birth Date boşken aktif olmamalı"
    def test_next_button_disabled_when_nat_id_is_empty(self):
        """National ID boş bırakıldığında Next butonu aktif olmamalı."""
        self.create_demografic_info.fill_demographic_info(
            first_name="Ahmet",
            middle_name="Ali",
            last_name="Yılmaz",
            father_name="Mehmet",
            mother_name="Ayşe",
            birth_date="01/01/1990",
            gender="Male",
            national_id=""  # Boş bırakılıyor
        )

        is_enabled = self.create_demografic_info.utils.is_button_enabled(self.create_demografic_info.NEXT_BUTTON)
        assert not is_enabled, "Next butonu National ID boşken aktif olmamalı"
    def test_nat_id_already_exists_validation(self):
        """19351229354 girildiğinde 'A customer already exists with this Nationality ID' uyarısı doğrulanmalı."""
        nat_id_input = self.create_demografic_info.CREATE_NATID
        self.create_demografic_info.utils.fill_input_field(nat_id_input, "19351229354")

        # Hata mesajının yüklenmesini bekle
        error_locator = (By.ID, "di-nationalid-err-taken")
        error_element = self.create_demografic_info.utils.wait_for_element(error_locator)

        assert error_element is not None, "Hata mesajı elementi bulunamadı"
        assert error_element.is_displayed(), "Hata mesajı görünür olmalı"
        assert error_element.text == "A customer already exists with this Nationality ID", \
            "Hata mesajı içeriği beklenenle eşleşmiyor"
    from datetime import datetime, timedelta

    def test_birth_date_under_18_shows_validation_message(self):
        """Kişi 18 yaşından küçükse 'Please enter a valid value' uyarısı görünmeli."""

        # Bugünden 17 yıl 11 ay önceye giderek 18 yaş altı bir tarih üret
        underage_date = (datetime.today() - timedelta(days=17*365 + 330)).strftime("%d/%m/%Y")

        self.create_demografic_info.fill_demographic_info(
            first_name="Ahmet",
            middle_name="Ali",
            last_name="Yılmaz",
            father_name="Mehmet",
            mother_name="Ayşe",
            birth_date=underage_date,
            gender="Male",
            national_id="12345678912"
        )

        error_locator = (By.ID, "di-birthdate-err-required")
        error_element = self.create_demografic_info.utils.wait_for_element(error_locator)

        assert error_element is not None, "18 yaş altı uyarı elementi bulunamadı"
        assert error_element.is_displayed(), "18 yaş altı uyarı mesajı görünür olmalı"
        assert error_element.text == "Please enter a valid value", "Uyarı metni beklenenle eşleşmiyor"

    from datetime import datetime, timedelta

    def test_birth_date_in_future_shows_validation_message(self):
        """Bugünün 5 gün sonrası girildiğinde 'Date cannot be in the future' uyarısı doğrulanmalı."""

        # Bugünden 5 gün ileriye giderek tarih üret
        future_date = (datetime.today() + timedelta(days=5)).strftime("%d/%m/%Y")

        self.create_demografic_info.fill_demographic_info(
            first_name="Ahmet",
            middle_name="Ali",
            last_name="Yılmaz",
            father_name="Mehmet",
            mother_name="Ayşe",
            birth_date=future_date,
            gender="Male",
            national_id="12345678912"
        )

        error_locator = (By.ID, "di-birthdate-err-future")
        error_element = self.create_demografic_info.utils.wait_for_element(error_locator)

        assert error_element is not None, "Gelecek tarih uyarı elementi bulunamadı"
        assert error_element.is_displayed(), "Gelecek tarih uyarı mesajı görünür olmalı"
        assert error_element.text == "Date cannot be in the future", "Uyarı metni beklenenle eşleşmiyor"
    def test_navigates_to_address_page_after_valid_demographic_info(self):
        """Tüm alanlar doğru doldurulduğunda Next'e tıklanmalı ve Address sayfasına geçilmeli."""

        # Tüm alanlara geçerli veri gir
        self.create_demografic_info.fill_demographic_info(
            first_name="Ahmet",
            middle_name="Ali",
            last_name="Yılmaz",
            father_name="Mehmet",
            mother_name="Ayşe",
            birth_date="01/01/1990",
            gender="Male",
            national_id="12345678912"
        )

        # Next butonuna tıkla
        self.create_demografic_info.utils.click_element(self.create_demografic_info.NEXT_BUTTON)

        # Address sayfası objesini oluştur
        create_address_page = CreateAddressPage(self.create_demografic_info.driver, self.create_demografic_info.wait)

        # Adres sayfasındaki butonun görünür olduğunu doğrula
        is_visible = create_address_page.utils.is_element_visible(create_address_page.CREATE_ADDRESS_BUTTON)
        assert is_visible, "Adres sayfasına geçildiği doğrulanmalı (CREATE_ADDRESS_BUTTON görünmeli)"
