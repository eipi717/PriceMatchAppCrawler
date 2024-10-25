import os

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from utils.web_driver_utils import init_driver, sleep_in_random_time
from services import generative_ai_services, http_services
import json
from utils.formatting_utils import get_product_dict, get_price_dict, get_history_price_dict
from selenium.common.exceptions import NoSuchElementException
import re

load_dotenv()


def get_urls() -> dict:
    categories = ['FRUIT_AND_VEGETABLES', 'MEAT', 'DELI_AND_PREPARED_MEALS', 'FISH_AND_SEAFOOD', 'DAIRY_AND_EGGS',
                  'BEVERAGES', 'BAKERY', 'HOUSEHOLD', 'FROZEN_FOODS', 'PANTRY', 'SNACKS', 'PERSONAL_CARE_AND_BEAUTY',
                  'BABY']
    return {category: os.getenv(f'FOODBASICS_{category}') for category in categories}


def navigate_to_items_page(web_driver: WebDriver, url: str):
    web_driver.get(url=url.format(1))
    sleep_in_random_time()


def get_number_of_pages(web_driver: WebDriver) -> int:
    page_button_class_name = 'ppn--element'
    page_buttons = web_driver.find_elements(By.CLASS_NAME, page_button_class_name)
    page_buttons = page_buttons[1:-1]
    return int(page_buttons[-1].text) if len(page_buttons) > 0 else 1


def get_products(web_driver: WebDriver) -> list:
    return web_driver.find_elements(By.CSS_SELECTOR,
                                    '.default-product-tile.tile-product.item-addToCart.tile-product--effective-date')


def extract_product_information(products: list, category: str) -> tuple[list[dict], list[dict], list[dict]]:
    product_list, price_list, history_price_list = [], [], []
    product_names = []

    for product in products:
        product_name = product.find_element(By.CLASS_NAME, 'head__title').text
        product_name = re.sub(r"'s|\s*'", "", product_name)
        product_names.append(product_name)

        product_image_outer = product.find_element(By.CLASS_NAME, 'pt__visual')
        product_image = product_image_outer.find_element(By.TAG_NAME, 'picture').find_element(By.TAG_NAME,
                                                                                              'img').get_attribute(
            'src')

    # put all product names to gen AI once only
    # Convert the string list into list of string by converting to valid json
    # TODO: Try catch --> if error -> re-gen again.
    # Process product names with Generative AI
    if len(product_names) != 0:
        processed_product_names = generative_ai_services.call_local_gemma(json.dumps(product_names))
        if not processed_product_names:
            print("No processed product names returned.")
            return product_list, price_list, history_price_list

        for product, processed_name in zip(products, processed_product_names):
            price_outer = product.find_element(By.CSS_SELECTOR, '.pricing__sale-price.promo-price')

            try:
                price: str = price_outer.find_elements(By.CLASS_NAME, 'price-update')[-1].text
            except NoSuchElementException:
                price: str = price_outer.find_elements(By.TAG_NAME, 'span')[-1].text

            price = price.split("$")[-1].replace(" ", "")

            price_per_unit_outer = product.find_element(By.CLASS_NAME, 'pricing__secondary-price')

            price_per_unit_and_unit: str = price_per_unit_outer.find_elements(By.TAG_NAME, 'span')[-1].text

            price_per_unit = price_per_unit_and_unit.replace(" ", "").split("/")[0].replace("$", "")

            unit = price_per_unit_and_unit.split("/")[-1].replace(" ", "").replace(".", "")

            product_name = product.find_element(By.CLASS_NAME, 'head__title').text

            try:
                size: str = product.find_element(By.CLASS_NAME, 'head__unit-details').text
                size = size.replace(" ", "")
            except NoSuchElementException:
                size = ""

            product_list.append(
                get_product_dict(product_name=product_name, product_category=category, product_image=product_image))
            price_list.append(get_price_dict(product_name=product_name, store_name="FoodBasics", price=price,
                                             price_per_unit=price_per_unit, unit=unit, size=size))
            history_price_list.append(
                get_history_price_dict(product_name=product_name, store_name="FoodBasics", price=price, unit=unit,
                                       price_per_unit=price_per_unit))

    return product_list, price_list, history_price_list


def extract_food_basics(web_driver: WebDriver):
    urls = get_urls()

    for category, url in urls.items():
        print(f'Extracting food basics for {category}')
        navigate_to_items_page(web_driver=web_driver, url=url)

        number_of_pages = get_number_of_pages(web_driver=web_driver)

        if category == 'PREPARED_MEALS' or category == 'DELI':
            category = 'DELI_AND_PREPARED_MEALS'

        for page_number in range(1, number_of_pages + 1):
            web_driver.get(url.format(page_number))

            sleep_in_random_time()

            products = get_products(web_driver=web_driver)

            list_of_products, list_of_prices, list_of_history_prices = extract_product_information(products=products,
                                                                                                   category=category)

            http_services.create_products(list_of_products=list_of_products)

            http_services.create_prices(list_of_prices=list_of_prices)

            http_services.create_history_prices(list_of_prices=list_of_history_prices)


if __name__ == '__main__':
    driver = init_driver()

    extract_food_basics(web_driver=driver)
