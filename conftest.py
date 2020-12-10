import os

import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


@pytest.fixture(scope='function')
def browser():
    caps = DesiredCapabilities.CHROME
    caps['loggingPrefs'] = {'performance': 'ALL'}
    options = Options()
    options.add_experimental_option('w3c', False)
    driver = Chrome(executable_path=f'{os.getcwd().split("src")[0]}chromedriver',
                    desired_capabilities=caps, options=options)
    driver.implicitly_wait(2)
    driver.maximize_window()
    yield driver
    driver.quit()
