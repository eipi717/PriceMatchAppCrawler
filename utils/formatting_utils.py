from utils.date_time_utils import to_date, get_flyers_start_date_thursday, get_flyers_end_date_wednesday


def get_product_dict(product_name: str, product_category: str, product_image: str) -> dict:
    return {
        'productName': product_name,
        'productCategory': product_category,
        'productImage': product_image
    }


def get_price_dict(product_name: str, store_name: str, price_per_unit: float, price: float, unit: str, size: str):
    return {
        'productName': product_name,
        'storeName': store_name,
        'price': price,
        'size': size,
        'pricePerUnit': price_per_unit,
        'unit': unit,
        'startDate': to_date(get_flyers_start_date_thursday()),
        'endDate': to_date(get_flyers_end_date_wednesday())
    }


def get_history_price_dict(product_name: str, store_name:str, price: float, price_per_unit: float, unit: str):
    return {
        "productName": product_name,
        "storeName": store_name,
        "price": price,
        "pricePerUnit": price_per_unit,
        "unit": unit,
        "dateOfPrice": get_flyers_start_date_thursday().timestamp()
    }
