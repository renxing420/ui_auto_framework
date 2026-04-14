from datetime import datetime
import os

import pytest
import yaml
import allure

from pages.base_page import BasePage
from utils.driver_factory import create_driver
import time
@pytest.fixture(scope="session")
def config():
    with open("config/config.yaml") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="function")
def driver(config):
    driver = create_driver(config)
    yield driver
    driver.quit()

# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item):
#     outcome = yield
#     report = outcome.get_result()
#     if report.failed:
#         driver = item.funcargs.get("driver")
#         if driver:
#             allure.attach(
#                 driver.get_screenshot_as_png(),
#                 name="失败截图",
#                 attachment_type=allure.attachment_type.PNG
#             )
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    yield
    if call.when == "call" and call.excinfo:
        driver = item.funcargs.get("driver")
        if driver:
            BasePage(driver).attach_screenshot("失败现场")