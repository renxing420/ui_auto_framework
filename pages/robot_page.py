import time

import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from utils.step_context import step

class RobotPage(BasePage):

    MENU_MANAGER = (By.XPATH,"//p[text()='管理中心']")
    MENU_ROBOT = (By.XPATH, "(//p[text()='机器人管理'])[last()]")
    CREATE_BTN = (By.XPATH, "//button[contains(.,'创建机器人')]")

    NAME_INPUT = (By.ID, "qaRobotName")
    KB_INPUT = (By.ID, "react-select-qa_robot-input")

    SUBMIT_BTN = (By.XPATH, "//button[contains(.,'确定')]")

    @step("进入管理中心")
    def go_to_manager_center(self):
        self.click(*self.MENU_MANAGER)

    @step("进入机器人管理")
    def go_to_robot_page(self):
        self.click(*self.MENU_ROBOT)

    @step("点击创建机器人")
    def click_create(self):
        self.click(*self.CREATE_BTN)
        self.wait_visible(self.NAME_INPUT)

    def find_clickable_visible(self, by, locator):
        elements = self.wait.until(lambda d: d.find_elements(by, locator))

        for el in elements:
            if el.is_displayed() and el.is_enabled():
                return el

        raise Exception(f"没有找到可点击元素: {locator}")

    @step("选择知识库")
    def select_knowledge_base(self, kb_name=None):
        with allure.step("选择知识库"):
            # 1️⃣ 点击输入框
            input_el = self.find_clickable_visible(By.ID, "react-select-qa_robot-input")
            input_el.click()
            # 2️⃣ 可选：输入过滤
            if kb_name:
                input_el.send_keys(kb_name)
            # 3️⃣ 等待下拉出现（关键）
            self.wait.until(
                lambda d: len(d.find_elements(By.XPATH, "//div[@role='option']")) > 0
            )
            # 4️⃣ 只选可见的 option
            options = self.driver.find_elements(By.XPATH, "//div[@role='option']")
            for opt in options:
                if opt.is_displayed():
                    text = opt.text.strip()
                    print("选择知识库:", text)
                    # 如果指定名称 → 精确匹配
                    if kb_name:
                        if kb_name in text:
                            opt.click()
                            return
                    else:
                        # 默认选第一个
                        opt.click()
                        return
            raise Exception("没有找到可选的知识库")

    @step("创建机器人")
    def create_robot(self, name):
        self.input(*self.NAME_INPUT, name)
        self.select_knowledge_base()
        self.click(*self.SUBMIT_BTN)
        # ⭐ 等待弹窗关闭（关键）
        self.wait.until(
            lambda d: len(d.find_elements(By.ID, "qaRobotName")) == 0
        )

    def is_robot_exist(self, name):
        elements = self.driver.find_elements(
            By.XPATH,
            f"//*[contains(text(),'{name}')]"
        )

        for el in elements:
            if el.is_displayed():
                return True
        return False

    def refresh_list(self):
        self.driver.refresh()
        time.sleep(1)

    @step("删除机器人")
    def delete_robot(self, name):
        # 找到对应行的删除按钮
        delete_btn = self.find_clickable_visible(
            By.XPATH,
            f"//*[text()='{name}']/ancestor::*//button[contains(.,'删除')]"
        )
        delete_btn.click()
        # 点击确认
        confirm_btn = self.find_clickable_visible(
            By.XPATH, "//button[contains(.,'确定')]"
        )
        confirm_btn.click()
        # self.attach_screenshot("删除机器人")
        # 等待消失
        self.wait.until(
            lambda d: not self.is_robot_exist(name)
        )