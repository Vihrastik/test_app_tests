import random

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import settings


class BasePageLocators:
    button = (By.XPATH, '//*[contains(@class, "btn")]', 'кнопка')


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = settings.BASE_URL

    def find_element(self, locator: tuple, time: int = 10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator[:2]),
                                                      message=f'Не получается найти элемент {locator[2]} '
                                                              f'на странице {self.driver.current_url}')

    def find_elements(self, locator: tuple, time: int = 10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator[:2]),
                                                      message=f'Не получается найти элемент {locator[2]} '
                                                              f'на странице {self.driver.current_url}')

    def is_locator_displayed(self, locator: tuple):
        try:
            return self.find_element(locator).is_displayed()
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException, TimeoutError):
            return False

    def is_clickable(self, locator: WebElement):
        return 'disabled' not in locator.get_attribute('class')

    def open(self):
        return self.driver.get(self.base_url)

    def get_random_button_id(self):
        buttons = self.find_elements(BasePageLocators.button)
        return random.choice(buttons).get_attribute('id')

    def get_random_button(self):
        buttons = self.find_elements(BasePageLocators.button)
        return random.choice(buttons)

    def check_button(self, text, button_id, is_clickable):
        buttons = self.find_elements(BasePageLocators.button)
        for button in buttons:
            if text == button.text:
                assert self.is_clickable(button) == is_clickable
                assert button.get_attribute('id') == str(button_id)

    def click_button(self, text):
        buttons = self.find_elements(BasePageLocators.button)
        for button in buttons:
            if text in button.text:
                button.click()
                break
