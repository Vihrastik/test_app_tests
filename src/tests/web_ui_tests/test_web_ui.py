import random

from src.common.funcs import (
    create_templ_with_one_button_not_clickable,
    create_templ_with_one_button_clickable,
    create_templ_with_hundred_button_clickable,
    create_templ_with_large_button_clickable,
    delete_all_templates,
)
from src.common.page import BasePage


class TestBasePage:

    def test_check_page_with_one_button_not_clickable(self, browser):
        create_templ_with_one_button_not_clickable()
        page = BasePage(browser)
        page.open()
        page.check_button(text='test', button_id=1, is_clickable=False)

    def test_check_page_with_one_button_clickable(self, browser):
        create_templ_with_one_button_clickable()
        page = BasePage(browser)
        page.open()
        page.check_button(text='test', button_id=1, is_clickable=True)
        page.click_button(text='test')
        assert 'test_link' in browser.current_url

    def test_check_page_with_hundred_button_clickable(self, browser):
        create_templ_with_hundred_button_clickable()
        page = BasePage(browser)
        page.open()
        button_number = page.get_random_button_id()
        page.check_button(text=f'test_label{button_number}', button_id=button_number, is_clickable=True)
        page.click_button(text=f'test_label{button_number}')
        assert f'test_link{button_number}' in browser.current_url

    def test_check_page_with_large_button_clickable(self, browser):
        create_templ_with_large_button_clickable()
        page = BasePage(browser)
        page.open()
        button = page.get_random_button()
        assert button.is_displayed()

    def test_check_change_template(self, browser):
        create_templ_with_one_button_not_clickable()
        page = BasePage(browser)
        page.open()
        page.check_button(text='test', button_id=1, is_clickable=False)
        create_templ_with_hundred_button_clickable()
        browser.refresh()
        button_number = random.randint(1, 10)
        page.check_button(text=f'test_label{button_number}', button_id=button_number, is_clickable=True)

    def test_delete_template(self, browser):
        create_templ_with_one_button_clickable()
        page = BasePage(browser)
        page.open()
        delete_all_templates()
        page.check_button(text='test', button_id=1, is_clickable=True)
        page.click_button(text='test')
        assert 'test_link' in browser.current_url
