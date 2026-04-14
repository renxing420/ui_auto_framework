import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_driver(config):
    browser = config.get("browser", "chrome")

    if browser == "chrome":
        options = Options()

        # ⭐ CI无头模式
        if config.get("headless", False):
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        # ⭐ 必加（否则CI容易点不到）
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.implicitly_wait(config.get("timeout", 10))
    return driver
