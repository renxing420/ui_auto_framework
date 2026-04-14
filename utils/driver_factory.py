import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_driver(config):
    browser = config.get("browser", "chrome")

    if browser == "chrome":
        options = Options()

        # ✅ 判断是否在 CI 环境
        is_ci = os.getenv("CI") == "true"

        # ✅ config 或 CI 任意一个满足，就开启无头
        if config.get("headless", False) or is_ci:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")   # 更稳
            print("CI:", os.getenv("CI"), "HEADLESS:", config.get("headless"))
        # ✅ 必加
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.implicitly_wait(config.get("timeout", 10))
    return driver