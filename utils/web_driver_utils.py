from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver, Options
import time
import random


def init_driver() -> WebDriver:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)

    return driver


def sleep_in_random_time():
    time.sleep(random.randint(5, 8))
