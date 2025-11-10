import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from constants.timeouts import DEFAULT_TIMEOUT

logger = logging.getLogger(__name__)


class Utils:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def wait_for_element(self, locator, timeout=DEFAULT_TIMEOUT):
        """Wait for an element to be present on the page."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            logger.warning(f"Element not found: {locator}")
            return None

    def click_element(self, locator, timeout=DEFAULT_TIMEOUT):
        """Wait for an element to be clickable and then click it."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except TimeoutException:
            logger.warning(f"Element not clickable: {locator}")

    def get_element_text(self, locator, timeout=DEFAULT_TIMEOUT):
        """Wait for an element to be visible and return its text."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.text.strip()
        except TimeoutException:
            logger.warning(f"Text not found for element: {locator}")
            return ""

    def is_element_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        """Check if an element is visible on the page."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def fill_input_field(self, locator, text, timeout=DEFAULT_TIMEOUT):
        """Wait for an input field to be present and fill it with text."""
        element = self.wait_for_element(locator, timeout)
        if element:
            element.clear()
            element.send_keys(text)
        else:
            logger.warning(f"Unable to fill input field: {locator}")

    def is_button_enabled(self, locator, timeout=DEFAULT_TIMEOUT):
        """Check if a button is enabled."""
        element = self.wait_for_element(locator, timeout)
        if element:
            return element.is_enabled()
        logger.warning(f"Button not found or not enabled: {locator}")
        return False

    def get_input_type(self, locator, timeout=DEFAULT_TIMEOUT):
        """Return the 'type' attribute of an input element."""
        element = self.wait_for_element(locator, timeout)
        if element:
            return element.get_attribute("type")
        logger.warning(f"Cannot get type attribute for: {locator}")
        return None
