import os

import google.generativeai as genai
import requests
import PIL.Image
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMMA_ENDPOINTS = os.getenv("GEMMA_ENDPOINTS")

GEMMA_MODEL = os.getenv("GEMMA_MODEL")


def get_system_prompt_for_product_name_standardization() -> str:
    return """
    You are a data analyst tasked with standardizing product names. You will receive a JSON array of product name strings as input. Follow the rules below to ensure consistency and clarity:

    1. Preserve Brand and Product Names:** Keep branded terms unchanged as they are essential for identity and recognition.
    2. Consistent Order:** Arrange terms logically, typically starting with the brand name followed by descriptive components such as flavor, type, or key attributes.
    3. Normalize Capitalization:** Capitalize the first letter of each main word (e.g., "Organic Apple Juice").
    4. Remove Redundant Punctuation and Symbols:** Eliminate unnecessary commas, periods, apostrophes, or other symbols that do not add clarity.
    5. Maintain Descriptive Elements:** Retain all descriptive terms that are crucial for accurately describing the product.
    6. One-to-One Transformation:** Ensure each input product name corresponds to exactly one standardized output.
    7. Output Format:** Return the standardized product names as a JSON array of strings. Do not include any additional formatting, explanations, or code.
    8. Maintain Input Structure:** Preserve the spacing provided in the input product names.
    9. Remove All Apostrophes:** For example, change "it's" to "its".
    10. Idempotent Standardization:** If a product name is already standardized, return it unchanged.
    11. Response Structure:** Provide only the list of standardized product names without any additional explanations, comments, or code snippets.
    12. Order Preservation:** The order of the standardized product names in the output list should match the order of the input product names.
    """


def call_local_gemma(list_of_product: str):
    response = requests.post(
        url=GEMMA_ENDPOINTS,
        json={
            "model": GEMMA_MODEL,
            "prompt": list_of_product,
            # We want one-time output
            "stream": False,
            # System prompt - setting rules
            "system": get_system_prompt_for_product_name_standardization()
        })
    return json.loads(response.json()['response'])



if __name__ == '__main__':
    testlist = [
        'Sweet Baby Peppers (4-Pack)', 'Extra Large Red Seedless Grapes', 'Pineapple',
        'Black Plums', 'Carrots', 'Gala Apples', 'Campari Tomatoes 1lb',
        'Yellow Potato', 'Pomegranate', 'Sweet Potato', 'Spaghetti Squash',
        'Butternut Squash', 'Grape Tomato', 'Celery Stalks', 'Spinach',
        'Romaine Heart', 'Yellow Onions', 'Brussels Sprouts',
        'Organics Baby Spinach', 'Pie Pumpkin', 'Roma Tomatoes',
        'Navel Oranges Cara Cara', 'White Potatoes', 'Fennel',
        'Variety Pack Tomatoes', 'Cabbage', 'Lemons', 'Rapini',
        'Plumcots', 'Acorn Squash', 'Beets', 'Buttercup Squash',
        'Parsnips', 'Field Greens Salad Mix'
    ]
    # standardized_list = call_local_gemma(testlist)
    # print("Type of standardized_list:", type(standardized_list))
    # print("Standardized Product Names:")
    # print(standardized_list)
    # call_gemini()

