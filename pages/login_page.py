from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.step_context import step

class LoginPage(BasePage):
    USERNAME = (By.XPATH, "//input[@placeholder='请输入用户名']")
    PASSWORD = (By.XPATH, "//input[@placeholder='请输入密码']")
    LOGIN_BTN = (By.XPATH, "//button[@type='submit']")

    @step("登录系统")
    def login(self, username, password):
        self.input(*self.USERNAME, text=username)
        self.input(*self.PASSWORD, text=password)
        self.click(*self.LOGIN_BTN)