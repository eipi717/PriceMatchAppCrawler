import os
import re

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from utils.web_driver_utils import init_driver, sleep_in_random_time
from services import generative_ai_services, http_services
from utils.formatting_utils import get_product_dict, get_price_dict, get_history_price_dict
import json

load_dotenv()


def get_urls() -> dict:
    categories = ['FRUIT_AND_VEGETABLES', 'MEAT', 'DELI', 'FISH_AND_SEAFOOD', 'DAIRY_AND_EGGS', 'BEVERAGES',
                  'PREPARED_MEALS', 'BAKERY', 'BEVERAGES', 'FROZEN_FOODS', 'PANTRY', 'SNACKS',
                  'OTHERS', 'HOME', 'HOUSEHOLD', 'PERSONAL_CARE_AND_BEAUTY', 'BABY', 'NATURAL_AND_ORGANIC']
    return {category: os.getenv(f'NOFRILLS_{category}') for category in categories}


def navigate_to_items_page(web_driver: WebDriver, url: str):
    web_driver.get(url=url.format(1))
    sleep_in_random_time()


def get_number_of_pages(web_driver: WebDriver) -> int:
    page_button_class_name = 'css-1f4yp4r'
    page_buttons = web_driver.find_elements(By.CLASS_NAME, page_button_class_name)
    return int(page_buttons[-1].text) if len(page_buttons) > 0 else 1


def get_products(web_driver: WebDriver) -> list:
    return web_driver.find_elements(By.CSS_SELECTOR, '.chakra-linkbox.css-yxqevf')


def extract_product_information(products: list, category: str) -> tuple[list[dict], list[dict], list[dict]]:
    product_list, price_list, history_price_list = [], [], []
    product_names = []

    # Put all product name into a list
    for product in products:
        product_name_outer = product.find_element(By.CSS_SELECTOR, '.chakra-heading.css-6qrhwc')
        product_name = product_name_outer.text.split(",")[0]
        product_name = re.sub(r"'s|\s*'", "", product_name)
        product_names.append(product_name)

    # put all product names to gen AI once only
    # Convert the string list into list of string by converting to valid json
    # TODO: Try catch --> if error -> re-gen again.
        # Process product names with Generative AI
    processed_product_names = generative_ai_services.call_local_gemma(json.dumps(product_names))
    if not processed_product_names:
        print("No processed product names returned.")
        return product_list, price_list, history_price_list

    # zip function gives tuple of the element: tuple(element_of_products, element_of_processed_product_names)
    for product, processed_name in zip(products, processed_product_names):
        try:
            price = product.find_element(By.CSS_SELECTOR, '.chakra-text.css-o93gbd').text.split("$")[-1].split(" ")[0]
        except NoSuchElementException:
            price = product.find_element(By.CSS_SELECTOR, '.chakra-text.css-pwnbcb').text.split("$")[-1].split(" ")[0]
        product_image = product.find_element(By.TAG_NAME, 'img').get_attribute('src')

        price_per_unit_outer = product.find_element(By.CSS_SELECTOR, '.chakra-text.css-1yftjin')
        if "," in price_per_unit_outer.text:
            size = price_per_unit_outer.text.split(",")[0]
            price_per_unit = price_per_unit_outer.text.split(",")[1].split("/")[0].replace("$", "").replace("ea", price).strip()
            unit = price_per_unit_outer.text.split(",")[1].split("/")[1]
        else:
            unit = price_per_unit_outer.text.split(" ")[-1]
            size = price_per_unit_outer.text.split(" ")[0]
            price_per_unit = price

        # Use the processed product name here
        product_list.append(get_product_dict(product_name=processed_name, product_category=category, product_image=product_image))
        price_list.append(get_price_dict(product_name=processed_name, store_name="NoFrills", price=price, price_per_unit=price_per_unit, unit=unit, size=size))
        history_price_list.append(get_history_price_dict(product_name=processed_name, store_name="NoFrills", price=price, unit=unit, price_per_unit=price_per_unit))
    return product_list, price_list, history_price_list


def extract_no_frills(web_driver: WebDriver):
    urls = get_urls()

    for category, url in urls.items():
        print(f'Extracting no_frills for {category}')
        navigate_to_items_page(web_driver=web_driver, url=url)

        number_of_pages = get_number_of_pages(web_driver=web_driver)
        print(f'number_of_pages: {number_of_pages}')

        if category == 'PREPARED_MEALS' or category == 'DELI':
            category = 'DELI_AND_PREPARED_MEALS'

        for page_number in range(1, number_of_pages + 1):
            web_driver.get(url.format(page_number))

            sleep_in_random_time()

            products = get_products(web_driver=web_driver)

            list_of_products, list_of_prices, list_of_history_prices = extract_product_information(products=products, category=category)

            http_services.create_products(list_of_products=list_of_products)

            http_services.create_prices(list_of_prices=list_of_prices)

            http_services.create_history_prices(list_of_prices=list_of_history_prices)


if __name__ == '__main__':
    driver = init_driver()

    extract_no_frills(web_driver=driver)
