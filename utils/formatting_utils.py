from utils.date_time_utils import to_date, get_flyers_wednesday_start_date, get_flyers_wednesday_end_date


def get_product_dict(product_name: str, product_category: str) -> dict:
    return {
        'productName': product_name,
        'productCategory': product_category
    }


def get_price_dict(product_name: str, store_name: str, price_per_unit: float, price: float, unit: str, size: str):
    return {
        'productName': product_name,
        'storeName': store_name,
        'price': price,
        'size': size,
        'pricePerUnit': price_per_unit,
        'unit': unit,
        'startDate': to_date(get_flyers_wednesday_start_date()),
        'endDate': to_date(get_flyers_wednesday_end_date())
    }


def get_history_price_dict(product_name: str, store_name:str, price: float, price_per_unit: float, unit: str, date_of_price: str, created_time: str):
    return {
        "productName": product_name,
        "storeName": store_name,
        "price": price,
        "pricePerUnit": price_per_unit,
        "unit": unit,
        "dateOfPrice": to_date(get_flyers_wednesday_start_date())
    }
