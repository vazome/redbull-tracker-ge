"""
Allows us to connect to platforms' APIs, parse JSON...
...Get system specific data, including time info and connect to PostgreSQL
"""

import json
import re
import os
from datetime import datetime
import requests
import pytz
import psycopg2

# Github Actions vars

PG_DB_CONNECTION = os.environ["PG_DB_CONNECTION"]
PG_DB_NAME = os.environ["PG_DB_NAME"]
PG_DB_PORT = os.environ["PG_DB_PORT"]
PG_PASSWORD = os.environ["PG_PASSWORD"]
PG_USER = os.environ["PG_USER"]

# Sometimes venues write names incorrectly like redbul...
# ...but platforms' search algorithms mitigate this issue.
REGEX_PATTERN = r"redbull|red bull|რედბულ|რედ ბულ"

# Creating an ISO 8601 compliant timestamp in UTC timezone
timezone = pytz.timezone("UTC")
time_in_tz = datetime.now(timezone)
timestr = time_in_tz.strftime("%Y-%m-%d-%H:%M:%S")

# Creating the dir if missing
EXPORT_DIR = "./export"
os.makedirs(EXPORT_DIR, exist_ok=True)

wolt_params_configs = {
    "en": {
        "q": "red bull",
        "target": "items",
        "lat": 41.6938026,
        "lon": 44.80151679999999,
        "sorting_and_filtering_v2": None,
    },
    "ge": {
        "q": "რედ ბულ",
        "target": "items",
        "lat": 41.6938026,
        "lon": 44.80151679999999,
        "sorting_and_filtering_v2": None,
    },
}

glovo_params_configs = {
    "ge": {"query": "რედ ბულ", "type": "Category"},
    "en": {"query": "red bull", "type": "Category"},
}


def wolt(wolt_config_key):
    wolt_url = "https://restaurant-api.wolt.com/v1/pages/search"
    wolt_headers = {
        "authority": "restaurant-api.wolt.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en;q=0.9",
        "app-language": "en",
        "client-version": "1.10.145",
        "clientversionnumber": "1.10.145",
        "content-type": "application/json",
        "origin": "https://wolt.com",
        "platform": "Web",
        "referer": "https://wolt.com/",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "w-wolt-session-id": "2483c231-b48b-465e-815e-57af0935ec52",
        "x-wolt-web-clientid": "d4c8fb08-64b8-4a23-9559-edf2e18a1858",
    }
    wolt_params = wolt_params_configs[wolt_config_key]
    wolt_post = requests.post(url=wolt_url, headers=wolt_headers, json=wolt_params)
    # It's some sort of error handling referencing HTTP respose code
    if str(wolt_post.status_code).startswith(("1", "2", "3")):
        print("Wolt status code" + str(wolt_post.status_code))
        return wolt_post.text
    else:
        return print("encountered an error:\n" + wolt_post.text)
    # If python native error handling, for now not required.
    #    try:
    #    except Exception as e:
    #        logging.error(traceback.format_exc())


def glovo(glovo_config_key):
    glovo_url = "https://api.glovoapp.com/v3/feeds/search"
    glovo_headers = {
        "authority": "api.glovoapp.com",
        "accept": "application/json",
        "accept-language": "en;q=0.9",
        "glovo-api-version": "14",
        "glovo-app-development-state": "Production",
        "glovo-app-platform": "web",
        "glovo-app-type": "customer",
        "glovo-app-version": "7",
        "glovo-client-info": "web-customer-web/7 project:customer-web",
        "glovo-delivery-location-accuracy": "0",
        "glovo-delivery-location-latitude": "41.69406499999999",
        "glovo-delivery-location-longitude": "44.8015793",
        "glovo-delivery-location-timestamp": "1706885996583",
        "glovo-device-urn": "glv:device:3d3572ae-231a-40de-a411-d2c99809aacb",
        "glovo-dynamic-session-id": "39c26e98-6ab8-49e4-addd-a264fc271b3d",
        "glovo-language-code": "en",
        "glovo-location-city-code": "TBI",
        "glovo-request-id": "cf38a368-e90a-4c7d-8c3a-b8e6fe575abc",
        "origin": "https://glovoapp.com",
        "referer": "https://glovoapp.com/",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }
    glovo_params = glovo_params_configs[glovo_config_key]
    glovo_get = requests.get(url=glovo_url, headers=glovo_headers, params=glovo_params)
    print("Glovo status code" + str(glovo_get.status_code))
    return glovo_get.text


# Sending data to a PostgreSQL
def pg_export(*datasets):
    connect = psycopg2.connect(
        database=PG_DB_NAME,
        user=PG_USER,
        host=PG_DB_CONNECTION,
        password=PG_PASSWORD,
        port=PG_DB_PORT,
    )
    SQL_EXPORT_GENERAL = """INSERT INTO general(venue_id, venue_name, product_id, platform_name)
    VALUES(%s, %s, %s, %s)
    ON CONFLICT (product_id) DO NOTHING"""
    SQL_EXPORT_PRODUCTS = """INSERT INTO products(product_id, product_name, product_price, product_description)
    VALUES(%s, %s, %s, %s)"""
    try:
        cursor = connect.cursor()
        # .executemany can only take a list or a tuple types
        # so we converting the dictionary into a tuple
        # with list comprehension, which performance is better the bigger the object
        for table_general_dict_data in datasets:
            table_general_tuple_data = [
                (
                    item["venue_id"],
                    item["venue_name"],
                    item["product_id"],
                    item["platform_name"],
                )
                for item in table_general_dict_data
            ]
            cursor.executemany(SQL_EXPORT_GENERAL, table_general_tuple_data)
        for table_products_dict_data in datasets:
            table_products_tuple_data = [
                (
                    item["product_id"],
                    item["product_name"],
                    item["product_price"],
                    item["product_description"],
                )
                for item in table_products_dict_data
            ]
            cursor.executemany(SQL_EXPORT_PRODUCTS, table_products_tuple_data)
        connect.commit()
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        connect.rollback()
    finally:
        cursor.close()
        connect.close()


# Parsing the data
results_glovo = {}
export_array = []
glovo_export_array = []
for key in glovo_params_configs:
    results_glovo[key] = glovo(key)
    #   print(results_wolt[key])
    glovo_json = json.loads(results_glovo[key])
    for element in glovo_json["elements"]:
        if element["singleData"]["type"] == "STORE_WITH_PRODUCTS":
            glovo_venue_id = element["singleData"]["storeProductsData"]["store"][
                "store"
            ]["id"]
            glovo_venue_name = element["singleData"]["storeProductsData"]["store"][
                "store"
            ]["name"]
            for product in element["singleData"]["storeProductsData"]["products"]:
                if re.findall(REGEX_PATTERN, product["name"], flags=re.I):
                    globo_product_id = product["id"]
                    glovo_product_name = product["name"]
                    glovo_product_description = product["description"]
                    glovo_product_price = str(round(product["price"], 2))
                    glovo_export = {
                        "venue_id": glovo_venue_id,
                        "venue_name": glovo_venue_name,
                        "product_id": globo_product_id,
                        "product_name": glovo_product_name,
                        "product_description": glovo_product_description,
                        "product_price": glovo_product_price,
                        "platform_name": "glovo",
                    }
                    glovo_export_array.append(glovo_export)

results_wolt = {}  # we create dict to destinguish en and ge keys
wolt_export_array = []
for key in wolt_params_configs:
    results_wolt[key] = wolt(key)
    #   print(results_wolt[key])
    wolt_json = json.loads(results_wolt[key])
    for section in wolt_json["sections"]:
        for item in section["items"]:
            wolt_venue_id = item["link"]["menu_item_details"]["venue_id"]
            wolt_venue_name = item["link"]["menu_item_details"]["venue_name"]
            wolt_product_id = item["link"]["menu_item_details"]["id"]
            wolt_product_name = item["link"]["menu_item_details"]["name"]
            wolt_product_description = item["link"]["menu_item_details"]["description"]
            wolt_product_price = item["link"]["menu_item_details"]["price"]
            wolt_export = {
                "venue_id": wolt_venue_id,
                "venue_name": wolt_venue_name,
                "product_id": wolt_product_id,
                "product_name": wolt_product_name,
                "product_description": wolt_product_description,
                "product_price": wolt_product_price / 100,
                "platform_name": "wolt",
            }
            wolt_export_array.append(wolt_export)

# Send to pgsql
pg_export(glovo_export_array, wolt_export_array)

# Additionally, saving data to a timestamped JSON file
with open(f"{EXPORT_DIR}/export_{timestr}.json", "w", encoding="utf-8") as f:
    json.dump(wolt_export_array, f, ensure_ascii=False, indent=4)
    json.dump(glovo_export_array, f, ensure_ascii=False, indent=4)
