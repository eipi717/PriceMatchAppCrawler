import os

import google.generativeai as genai
import requests

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMMA_ENDPOINTS = os.getenv("GEMMA_ENDPOINTS")

GEMMA_MODEL = os.getenv("GEMMA_MODEL")


def get_system_prompt_for_product_name_standardization() -> str:
    return """
    imagine you are a data analyst. Your task now is standardize the product names by using the rules below:
    1. Preserve Brand and Product Names: Keep branded terms like "Health Break" as they are crucial for identity and recognition.
    2. Consistent Order: Maintain a logical order of terms which typically starts with the brand name followed by the descriptive components (flavor, type, key attributes).
    3. Normalize Capitalization: Convert all letters to standard capitalization where the first letter of each main word is capitalized (e.g., "Berry Pomegranate Antioxidant Juice"), which is common in product labeling.
    4. Remove Redundant Punctuation and Symbols: Exclude any unnecessary commas or other symbols that do not contribute to the clarity or meaning.
    5. Keep Descriptive Elements: Retain descriptive terms such as "Berry Pomegranate" and "Antioxidant Juice" as they are integral to describing the product.
    6. Confirm that it is one-to-one transformation, i.e. one input gives one output only.
    7. Please return the result only in pure produce name string and split by |. So that I can use python split function to get the product name one by one
                """


def get_ai_response_for_product_name_and_category(products_name_with_brand: list):
    genai.configure(api_key=GEMINI_API_KEY)

    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)

    model = genai.GenerativeModel('gemini-pro-vision')

    message = """
    I am currently building a price storing application, and I would like to store the product with extracted name into database, but I've got a column called product category, would you mind to assign a standardize category for this product? However, make the product name as common as possible so that it will align with the data extracted from other pages. Please give me the answer in the form "product category,product name,price". Please give the answer back in json string format and only the json, with the field "product_name", "product_category" and "price". For the input, it is in dictionary with product name as key and price as value.

{"Leclerc-Go Pure Oatmeal Bars Brown Sugar & Maple (Limit 6- After Limit $2.99)": "$2.00", "Silver Hills-The Big 16": "$5.00", "President's Choice-Unsalted Peanuts": "$4.99", "Plums- Black or Red": "about", "Leclerc-Go Pure Fruit & Oat Bars Strawberry (Limit 6- After Limit $2.99)": "$2.00", "No Name-Farmer's Marble Cheese": "$7.99", "Nestl\u00e9-Christie Oreo Frozen Dessert Sandwiches- Creme-flavoured Frozen Dessert Mixed With OREO Cookie Pieces Is Sandwiched Between Two Big Oreo Cookie Wafers-": "$5.99", "Silk-Almond Beverage- Unsweetened Original- Dairy-Free": "$3.79", "Kiwis": "$0.79", "Seaquest-Cooked Shrimp- 36/45": "$4.99", "No Name-Bagel Poppy Seed": "$1.75", "Dried Turkish Apricots": "$1.99", "Coca-Cola-Diet - Bottle": "$1.99", "Farmer's Market-Red Grapefruit- 3 lb Bag": "$4.99", "Huggies-Little Movers Baby Diapers- Size 4 (22-37 lbs)- 58 Ct": "$19.99", "No Name-Pizza Mozzarella Cheese- 28% MF": "$7.99", "Ziggy's-Creamy Potato Salad": "$2.99", "Earths Own-Almond Beverage- Unsweetened Vanilla": "$3.49", "Pepsi-Diet Soda": "$1.99", "Silk-Almond Beverage- Original- Plant Based Dairy-Free Milk": "$3.79", "Leclerc-Go Pure Fruit & Oats Bars- Chocolate & Wild Blueberry (Limit 6- After Limit $2.99)": "$2.00", "Pepsi-Diet Soda Caffeine Free": "$1.99", "Leclerc-Go Pure Fruit & Oats Bars- Chocolate & Strawberry (Limit 6- After Limit $2.99)": "$2.00", "Grace-Caribbean Combos Rice & Red Kidney Beans Mix": "$1.99", "Silk-Organic Soy Beverage- Original- Dairy-Free": "$3.79", "Nature Clean-Laundry Liquid- Lavender Fields": "$13.49", "Dempster-100% Whole Wheat Bread": "$2.49", "The Laughing Cow-Garlic & Herb": "$3.99", "Fantastik-Disinfectant All-Purpose Cleaner with Bleach- Eliminates Stains": "$4.99", "Larabar-Fruit & Nut Energy Bar- Chocolate Chip- 16/pack": "$18.99", "Tetley-Green Tea The Vert Naturellement Decafeine": "$5.99", "Ziggy's-Buffalo-Style Chicken Breast Strips": "$6.00", "Black Diamond-Thick Processed Cheddar Cheese Slices- 22 units": "$2.49", "Cracker Barrel-Marble Cheddar Cheese Slices": "$4.49", "Suraj-Channa Dal": "$3.99", "Cracker Barrel-Herb & Garlic Cheddar Cheese Slices- 11 units": "$4.49", "Cracker Barrel-Old White Cheddar Cheese Slices- 11 units": "$4.49", "Grace-Caribbean Combos Rice & Blackeye Peas Mix": "$1.99", "Larabar-Fruit & Nut Energy Bar- Peanut Butter Chocolate Chip- 16/pack": "$18.99", "Suraj-3.25% M.F. Dahi Yogurt": "$2.29", "Dempster-White Bread": "$2.49", "Silk-Almond Beverage- Unsweetened- Vanilla Flavour- Dairy-Free": "$3.79", "Crispy-Almond Pound Cake": "$3.50", "Nestl\u00e9-Nesquik Milkshake": "$1.25", "Ruffles-Sour Cream 'n Onion Flavoured Potato Chips": "$3.99", "Nivea-Extra Nourishing Body Milk": "$8.49", "Canada Dry-Ginger Ale": "$11.49"}
"""

    response = model.generate_content(message).text

    print(response)

    # category = response.split(",")[0]
    #
    # product_name = response.split(",")[1].strip()
    #
    # print(category, product_name)
    #
    # return category, product_name


def call_local_gemma(list_of_product: str):
    response = requests.post(
        url=GEMMA_ENDPOINTS,
        json={
            "model": GEMMA_MODEL,
            "prompt": list_of_product,
            "stream": False,
            "system": get_system_prompt_for_product_name_standardization()
        })
    return response.json()['response']


def test_():
    import pandas as pd
    df = pd.read_csv('../PriceMatch_Backup_data/Product.csv')
    product_name_list = df['product_name'].tolist()

    portion: int = len(product_name_list) // 5

    for i in range(portion + 1):
        start = 5 * i
        product_name_sub_list = product_name_list[start: min(start + 5, len(product_name_list))]
        print(len(product_name_sub_list))
        result = call_local_gemma(list_of_product=str(product_name_sub_list))

        print(result)

    # result = call_local_gemma(str(product_name_list[:100]))

    # print(result)


if __name__ == '__main__':
    test_()

    a = ['Apple', 'Orange', 'Banana', 'Grape', 'Pear', 'Red Grapefruit', 'Kiwis', 'Dried Turkish Apricots', 'Plums',
         "D'Anjou Pears", 'Finger Hot Hot Peppers', 'Cilantro', 'Green Onion', 'Organics Whole Cremini Mushrooms',
         'Tomato On The Vine Red', 'Greenhouse Peppers', 'Honeydew Melon', 'Organic Dates', 'Mint', 'Fenugreek',
         'Grape Tomato', 'Yellow Onions', 'Dried Turkish Figs', 'Indian Eggplant', 'Ataulfo Mango', 'Gala Apples',
         'Red Peppers', 'Rapini', 'Bosc Pears', 'Red Thai Hot Peppers', 'Mini Cucumbers', 'Organic Strawberries',
         'Mandarin Oranges', 'Walnuts', 'Okra', 'Garlic Bulbs', 'Pitted Honey Dates', 'White Mushrooms',
         'Beyond Sausage Hot Italian', 'Angus Burger', 'Original Bratwurst Sausage', 'Sirloin Beef Burger',
         'Lean Beef Burgers', 'Hot Italian Sausage', 'Original Breakfast Sausage', 'Maple Breakfast Sausage',
         'Goat Stew Bone In', 'Red Hots Original Hot Dogs', 'Thick & Juicy™ Beef Burgers',
         'Thick & Juicy™ Chicken Burgers', 'Natural Top Dogs Original Hot Dogs', 'Honey Garlic Sausage',
         'Original Breakfast Sausage Rounds', 'Brown Sugar & Honey Breakfast Sausage', 'Lean Ground Pork',
         'Thick & Juicy™ Prime Rib Beef Burger', 'Wagyu Beef Burgers', 'Sirloin Tip Steak', 'Sausage Mild Italian',
         'Chicken Leg with Bone', 'Mild Italian Sausage', 'Cheddar Hot Dogs', 'Breakfast Sausage',
         'Thick & Juicy™ Sirloin Beef Burgers ', 'Umami Wagyu Burgers', 'Free From Angus Beef Burger', 'Garlic & Herb',
         'Buffalo-Style Chicken Breast Strips', 'Cheese', 'Lunch Mate Bologna Lunch Kit', 'Jalapeno',
         'Semi-Soft Ripened Cheese Mini Gouda Taste 24% M.F.', 'Chicken Breast Strips',
         'Lunch Mate Two Cheese Pizza Lunch Kit', 'Dry Cured Italian Dry Salami Snack Kit',
         'Dry Cured Genoa Salami Snack Kit', 'Swiss', 'Light', 'Original (6 x 20g)', 'Lunch Mate Turkey Lunch Kit',
         'Italian-Style Chicken Breast Strips', 'Lunch Mate Ham Lunch Kit', 'Turkey Breast Strips', 'Cheese Dippers',
         'Hardwood Smoked Turkey Breast Snack Kit', 'Lunch Mate Pizza Pepperoni Lunch Kit',
         'Lunch Mate Hot Dogs Lunch Kit', 'Creamy Potato Salad', 'Fettuccine', 'Rainbow Cheese Tortellini',
         'Macaroni Salad', 'Creamy Green Coleslaw', 'Cheese and Bacon Tortellini', 'Macaroni & Cheese Salad',
         'Lasagna Sheets Pasta', 'Linguine', 'Beef Tortellini', 'Cheese & Spinach Ravioli', 'Potato & Egg Salad',
         'Cooked Shrimp']
