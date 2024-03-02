"""
Allows us to connect to platforms' APIs, parse JSON...
...Get system specific data, including time info and connect to PostgreSQL
"""

import json
import re
import os
from datetime import datetime
import time
import requests
import pytz
import psycopg2
from psycopg2.extras import execute_batch

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
timestr = time_in_tz.strftime("%Y-%m-%d-%H-%M-%S")

# Creating the dir if missing
# Not required after docker implementation
# EXPORT_DIR = "./export"
# os.makedirs(EXPORT_DIR, exist_ok=True)
locations = {}
raw_array = {}
export_array = []
EXPORT_FILE = f"./export_{timestr}.csv"
header_row = "location_name\tvenue_id\tvenue_name\tproduct_id\tproduct_name\tproduct_description\tproduct_price\tplatform_name"


def get_data():
    with open(file="./requests_data.json", encoding="utf-8") as f:
        config = json.load(f)
        # Getting all location options and properly format them as dict
    for group_name, location_list in config["locations_async"].items():
        for location in location_list:
            # Extract the location name, and create a sub-dictionary with 'lat' and 'lon'
            location_name = location["name"]
            locations[location_name] = {
                "lat": location["lat"],
                "lon": location["lon"],
            }

        def request_by_type(method, **kwargs):
            request_method = getattr(requests, method)
            response = request_method(**kwargs)
            # print(platform["service_name"] + " status code" + str(response.status_code))
            # return response.text, platform["service_name"]
            # It's some sort of error handling referencing HTTP respose code
            return response

    for platform in config["platforms"]:
        platform_name = platform["platform_name"]
        if platform_name not in raw_array:
            raw_array[platform_name] = []
        for location_name, location_data in locations.items():
            if platform["platform_name"] == "wolt":
                for lang, params in platform["params_configs"].items():
                    special_none_thing = {"sorting_and_filtering_v2": None}
                    params_final = params | location_data | special_none_thing
                    time.sleep(5)
                    response = request_by_type(
                        platform["request_type"],
                        url=platform["url"],
                        headers=platform["headers"],
                        json=params_final,
                        timeout=60,
                    )
                    raw_array[platform_name].append(
                        {
                            "location_name": location_name,
                            "raw_data": response.text,
                        }
                    )

            if platform["platform_name"] == "glovo":
                # Renaming location key to the ones glovo expects
                location_data["glovo-delivery-location-latitude"] = location_data.pop(
                    "lat"
                )
                location_data["glovo-delivery-location-longitude"] = location_data.pop(
                    "lon"
                )
                # params_configs stores the queries, so we unpack it
                # Store key in variable "lang" (en, ge)
                # Store values in variable "params", these values, also have keys and values
                for lang, params in platform["params_configs"].items():
                    headers_final = location_data | platform["headers"]
                    time.sleep(5)
                    response = request_by_type(
                        platform["request_type"],
                        url=platform["url"],
                        headers=headers_final,
                        params=params,
                        timeout=60,
                    )
                    raw_array[platform_name].append(
                        {
                            "location_name": location_name,
                            "raw_data": response.text,
                        }
                    )
    return raw_array


# Parsing the data, I wanted it to be universal, but guess each platform will have their own function
def wolt_parse():
    for location in raw_array["wolt"]:
        location_name = location["location_name"]
        raw_data = json.loads(location["raw_data"])
        for sections in raw_data["sections"]:
            for item in sections["items"]:

                wolt_venue_id = item["link"]["menu_item_details"]["venue_id"]
                wolt_venue_name = item["link"]["menu_item_details"]["venue_name"]
                wolt_product_id = item["link"]["menu_item_details"]["id"]
                wolt_product_name = item["link"]["menu_item_details"]["name"]
                wolt_product_description = item["link"]["menu_item_details"][
                    "description"
                ]
                wolt_product_price = item["link"]["menu_item_details"]["price"]
                wolt_export = {
                    "location_name": location_name,
                    "venue_id": wolt_venue_id,
                    "venue_name": wolt_venue_name,
                    "product_id": wolt_product_id,
                    "product_name": wolt_product_name,
                    "product_description": wolt_product_description,
                    "product_price": wolt_product_price / 100,
                    "platform_name": "wolt",
                }
                export_array.append(wolt_export)


def glovo_parse():
    for location in raw_array["glovo"]:
        # Parsing the JSON string in 'raw_data' to a Python dict
        location_name = location["location_name"]
        raw_data = json.loads(location["raw_data"])
        if "elements" in raw_data:
            for element in raw_data["elements"]:
                if element["singleData"]["type"] == "STORE_WITH_PRODUCTS":
                    glovo_venue_id = element["singleData"]["storeProductsData"][
                        "store"
                    ]["store"]["id"]
                    glovo_venue_name = element["singleData"]["storeProductsData"][
                        "store"
                    ]["store"]["name"]
                    for product in element["singleData"]["storeProductsData"][
                        "products"
                    ]:
                        if re.findall(REGEX_PATTERN, product["name"], flags=re.I):
                            globo_product_id = product["id"]
                            glovo_product_name = product["name"]
                            glovo_product_description = product["description"]
                            glovo_product_price = str(round(product["price"], 2))
                            glovo_export = {
                                "location_name": location_name,
                                "venue_id": glovo_venue_id,
                                "venue_name": glovo_venue_name,
                                "product_id": globo_product_id,
                                "product_name": glovo_product_name,
                                "product_description": glovo_product_description,
                                "product_price": glovo_product_price,
                                "platform_name": "glovo",
                            }
                            export_array.append(glovo_export)


# Sending data to a PostgreSQL
def pg_export(data):
    connect = psycopg2.connect(
        database=PG_DB_NAME,
        user=PG_USER,
        host=PG_DB_CONNECTION,
        password=PG_PASSWORD,
        port=PG_DB_PORT,
    )
    SQL_EXPORT_GENERAL = """
    INSERT INTO general(venue_id, venue_name, product_id, product_name, platform_name)
    VALUES(%s, %s, %s, %s, %s)
    ON CONFLICT (product_id)
    DO UPDATE SET product_name = EXCLUDED.product_name
    WHERE general.product_name IS NULL"""
    SQL_EXPORT_PRODUCTS = """INSERT INTO products(location_name, product_id, product_name, product_price, product_description)
    VALUES(%s, %s, %s, %s, %s)"""
    cursor = connect.cursor()
    size = 100
    try:
        general_data = [
            (
                item["venue_id"],
                item["venue_name"],
                item["product_id"],
                item["product_name"],
                item["platform_name"],
            )
            for item in data
        ]
        products_data = [
            (
                item["location_name"],
                item["product_id"],
                item["product_name"],
                item["product_price"],
                item["product_description"],
            )
            for item in data
        ]
        execute_batch(cursor, SQL_EXPORT_GENERAL, general_data, page_size=size)
        execute_batch(cursor, SQL_EXPORT_PRODUCTS, products_data, page_size=size)

        connect.commit()
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        connect.rollback()
    finally:
        cursor.close()
        connect.close()


def main():
    get_data()
    glovo_parse()
    wolt_parse()
    with open(f"./export/export_{timestr}.json", "w", encoding="utf-8") as f:
        json.dump(export_array, f, ensure_ascii=False, indent=4)
    pg_export(export_array)


if __name__ == "__main__":
    main()
