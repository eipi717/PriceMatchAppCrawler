import requests
from dotenv import load_dotenv
import os

load_dotenv()

SERVER_DOMAIN = os.getenv('SERVER_DOMAIN')


def getAllPrice():
    response = requests.get(f'{SERVER_DOMAIN}/api/v1/prices/getAllPrices')

    print(response.json())


def create_products(list_of_products: list):
    response = requests.post(f'{SERVER_DOMAIN}/api/v1/products/createProduct', json=list_of_products)

    print(f"Product's API: {response.status_code}")


def create_prices(list_of_prices: list):
    response = requests.post(f'{SERVER_DOMAIN}/api/v1/prices/createPrice', json=list_of_prices)

    print(f"Price's API: {response.status_code}")


def create_history_prices(list_of_prices: list):
    response = requests.post(f'{SERVER_DOMAIN}/api/v1/historicalPrice/createHistoricalPrice', json=list_of_prices)

    print(f"History Price's API: {response.status_code}")
