import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.robot_page import RobotPage


@allure.feature("机器人管理")
@allure.story("创建机器人")
def test_create_robot(driver, config):

    login_page = LoginPage(driver)
    robot_page = RobotPage(driver)

    login_page.open(config["base_url"] + "/login")
    login_page.login("99999999999", "999999")
    time.sleep(2)

    robot_page.go_to_manager_center()
    time.sleep(1)

    robot_page.go_to_robot_page()
    robot_page.click_create()
    name = f"newRobot{int(time.time())}"
    robot_page.create_robot(name)
    time.sleep(1)

    robot_page.refresh_list()
    assert robot_page.is_robot_exist(name)

    robot_page.delete_robot(name)
    driver.quit()
