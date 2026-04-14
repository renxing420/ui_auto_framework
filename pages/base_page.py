import inspect
import os
from functools import wraps

from utils.step_context import step
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
import allure


class BasePage:

    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self._step_index = 0

    # def attach_screenshot(self, name="截图"):
    #     filename = f"{name}_{int(time.time())}.png"
    #     self.driver.save_screenshot(filename)
    #
    #     allure.attach.file(
    #         filename,
    #         name=name,
    #         attachment_type=allure.attachment_type.PNG
    #     )

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        # 只拦截方法
        if callable(attr) and not name.startswith("_"):
            @wraps(attr)
            def wrapper(*args, **kwargs):
                class_name = self.__class__.__name__
                # ⭐ 优先用装饰器定义的名字
                step_name = getattr(attr, "_step_name", f"{class_name}.{name}")
                if not step_name:
                    step_name = f"{class_name}.{name}"
                with allure.step(step_name):
                    result = attr(*args, **kwargs)
                    if hasattr(attr, "_step_name"):
                        self.attach_screenshot(step_name)
                    return result
            return wrapper
        return attr

    def attach_screenshot(self, step_name="step"):
        if not hasattr(self, "_step_index"):
            self._step_index = 0
        self._step_index += 1

        timestamp = int(time.time() * 1000)
        test_name = os.getenv("PYTEST_CURRENT_TEST", "test") \
                        .split(":")[-1].split(" ")[0]

        date_dir = time.strftime('%Y-%m-%d')
        dir_path = f"reports/screenshots/{date_dir}/{test_name}"
        os.makedirs(dir_path, exist_ok=True)

        file_name = f"{self._step_index:02d}_{step_name}_{timestamp}.png"
        file_path = os.path.join(dir_path, file_name)

        self.driver.save_screenshot(file_path)

        with open(file_path, "rb") as f:
            allure.attach(
                f.read(),
                name=f"{self._step_index:02d}_{step_name}",
                attachment_type=allure.attachment_type.PNG
            )

    def open(self, url):
        self.driver.get(url)
        # self.driver.maximize_window()

    def find(self, by, locator):
        return self.wait.until(EC.presence_of_element_located((by, locator)))

    def find_clickable(self, by, locator):
        return self.wait.until(EC.element_to_be_clickable((by, locator)))

    # def click(self, by, locator, retry=2):
    #     for i in range(retry):
    #         try:
    #             el = self.find_clickable(by, locator)
    #             el.click()
    #             return
    #         except StaleElementReferenceException:
    #             if i == retry - 1:
    #                 raise
    #             time.sleep(1)

    def click(self, by, locator, desc="点击"):
        el = self.find_clickable_visible(by, locator)

        with allure.step(f"{desc}: {locator}"):
            el.click()


    def find_clickable_visible(self, by, locator):
        elements = self.wait.until(lambda d: d.find_elements(by, locator))

        for el in elements:
            if el.is_displayed() and el.is_enabled():
                return el

        raise Exception(f"没有找到可点击元素: {locator}")


    def input(self, by, locator, text):
        el = self.find(by, locator)
        el.clear()
        el.send_keys(text)

    # def input(self, by, locator, text, desc="输入"):
    #     el = self.find_clickable_visible(by, locator)


    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def select_react_option(self, input_locator, text=None):
        el = self.find(*input_locator)
        el.click()
        if text:
            el.send_keys(text)
        option = ("xpath", "//div[@role='option']")
        self.wait.until(EC.visibility_of_element_located(option))
        self.driver.find_elements(*option)[0].click()

