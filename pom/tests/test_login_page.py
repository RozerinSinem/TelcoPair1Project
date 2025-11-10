import pytest
from pages.login_page import LoginPage
from pages.customer_search_page import CustomerSearchPage
from constants.credentials import (
    VALID_USERNAME,
    VALID_PASSWORD,
    INVALID_USERNAME,
    INVALID_PASSWORD
)


@pytest.mark.smoke
class TestLoginPage:

    def test_verify_login_page_elements(self, driver, wait):
        """Login ekranındaki Username, Password inputları ve Login butonunun görünürlüğünü doğrular."""
        login_page = LoginPage(driver, wait)
        login_page.load()

        assert login_page.utils.is_element_visible(login_page.USERNAME_INPUT), "Username input görünmüyor!"
        assert login_page.utils.is_element_visible(login_page.PASSWORD_INPUT), "Password input görünmüyor!"
        assert login_page.utils.is_element_visible(login_page.LOGIN_BUTTON), "Login butonu görünmüyor!"

    def test_login_button_disabled_if_fields_too_short(self, driver, wait):
        """Username veya password 2 karakterden az olduğunda Login butonu pasif olmalı."""
        login_page = LoginPage(driver, wait)
        login_page.load()

        login_page.utils.fill_input_field(login_page.USERNAME_INPUT, "a")
        login_page.utils.fill_input_field(login_page.PASSWORD_INPUT, "b")

        assert not login_page.utils.is_button_enabled(login_page.LOGIN_BUTTON), \
            "Login butonu aktif olmamalı (kısa inputlarla)!"

    def test_login_button_enabled_if_fields_valid(self, driver, wait):
        """Username ve password 2+ karakter olduğunda Login butonu aktif olmalı."""
        login_page = LoginPage(driver, wait)
        login_page.load()

        login_page.utils.fill_input_field(login_page.USERNAME_INPUT, VALID_USERNAME)
        login_page.utils.fill_input_field(login_page.PASSWORD_INPUT, VALID_PASSWORD)

        assert login_page.utils.is_button_enabled(login_page.LOGIN_BUTTON), \
            "Login butonu aktif olmalı!"

    def test_password_is_masked(self, driver, wait):
        """Şifre alanı maskelenmiş olmalı (type='password')."""
        login_page = LoginPage(driver, wait)
        login_page.load()

        login_page.utils.fill_input_field(login_page.PASSWORD_INPUT, VALID_PASSWORD)
        input_type = login_page.utils.get_input_type(login_page.PASSWORD_INPUT)

        assert input_type == "password", f"Şifre alanı maskelenmemiş! (type='{input_type}')"

    def test_password_visible_after_eye_icon_click(self, driver, wait):
        """Göz ikonuna tıklanınca şifre görünür hale gelmeli (type='text')."""
        login_page = LoginPage(driver, wait)
        login_page.load()

        login_page.utils.fill_input_field(login_page.PASSWORD_INPUT, VALID_PASSWORD)
        login_page.utils.click_element(login_page.EYE_ICON)

        input_type = login_page.utils.get_input_type(login_page.PASSWORD_INPUT)
        assert input_type == "text", f"Göz ikonuna tıklanınca şifre görünür hale gelmedi! (type='{input_type}')"

    def test_invalid_password_shows_error(self, driver, wait):
        """Doğru username + yanlış şifre => hata mesajı doğru görünmeli."""
        login_page = LoginPage(driver, wait)
        login_page.load()

        login_page.login(VALID_USERNAME, INVALID_PASSWORD)

        assert login_page.utils.is_element_visible(login_page.LOGIN_ALERT), \
            "Hatalı şifre sonrası hata mesajı görünmedi!"
        
        alert_text = login_page.utils.get_element_text(login_page.LOGIN_ALERT)
        expected_text = "Wrong username or password. Please try again"
        assert alert_text == expected_text, f"Beklenen mesaj: '{expected_text}', ama gelen: '{alert_text}'"

    def test_invalid_username_shows_error(self, driver, wait):
        """Yanlış username + doğru şifre => hata mesajı doğru görünmeli."""
        login_page = LoginPage(driver, wait)
        login_page.load()

        login_page.login(INVALID_USERNAME, VALID_PASSWORD)

        assert login_page.utils.is_element_visible(login_page.LOGIN_ALERT), \
            "Yanlış kullanıcı sonrası hata mesajı görünmedi!"
        
        alert_text = login_page.utils.get_element_text(login_page.LOGIN_ALERT)
        expected_text = "Wrong username or password. Please try again"
        assert alert_text == expected_text, f"Beklenen mesaj: '{expected_text}', ama gelen: '{alert_text}'"

    def test_invalid_both_shows_error(self, driver, wait):
        """Yanlış username + yanlış şifre => hata mesajı doğru görünmeli."""
        login_page = LoginPage(driver, wait)
        login_page.load()

        login_page.login(INVALID_USERNAME, INVALID_PASSWORD)

        assert login_page.utils.is_element_visible(login_page.LOGIN_ALERT), \
            "Yanlış bilgiler sonrası hata mesajı görünmedi!"
        
        alert_text = login_page.utils.get_element_text(login_page.LOGIN_ALERT)
        expected_text = "Wrong username or password. Please try again"
        assert alert_text == expected_text, f"Beklenen mesaj: '{expected_text}', ama gelen: '{alert_text}'"


    def test_successful_login_redirects_to_customer_page(self, driver, wait):
        """Başarılı giriş sonrası müşteri arama ekranındaki Search butonu görünmeli."""
        login_page = LoginPage(driver, wait)
        customer_page = CustomerSearchPage(driver, wait)

        login_page.load()
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        assert customer_page.utils.is_element_visible(customer_page.SEARCH_BUTTON), \
            "Login sonrası Search butonu görünmedi!"