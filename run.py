"""
Allows us to connect to platforms' APIs, parse dato to JSON and send it all to DB
"""

import json
import re
import os
from datetime import datetime
import random
import requests
from requests.adapters import HTTPAdapter, Retry

import pytz
import psycopg2
from psycopg2.extras import execute_batch

# Github Actions vars
PG_DB_CONNECTION = os.environ["PG_DB_CONNECTION"]
PG_DB_NAME = os.environ["PG_DB_NAME"]
PG_DB_PORT = os.environ["PG_DB_PORT"]
PG_PASSWORD = os.environ["PG_PASSWORD"]
PG_USER = os.environ["PG_USER"]

SQL_EXPORT_GENERAL = """
    INSERT INTO general(venue_id, venue_name, product_id, product_name, platform_name)
    VALUES(%s, %s, %s, %s, %s)
    ON CONFLICT (product_id)
    DO UPDATE SET product_name = EXCLUDED.product_name
    WHERE general.product_name IS NULL"""
SQL_EXPORT_PRODUCTS = """
    INSERT INTO products(location_name, product_id, product_name, product_price, product_description)
    VALUES(%s, %s, %s, %s, %s)"""

REGEX_PATTERN = r"redbull|red bull|რედბულ|რედ ბულ"

# Creating an ISO 8601 compliant timestamp in UTC timezone
timezone = pytz.timezone("UTC")
time_in_tz = datetime.now(timezone)
timestr = time_in_tz.strftime("%Y-%m-%d-%H-%M-%S")

# Parsing prerequisites
locations = {}
raw_array = {}
export_array = []
EXPORT_FILE = f"./export_{timestr}.csv"
get_proxies = requests.get(
    url="https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    timeout=10,
)


def setup_proxies():
    """
    Downloading fresh proxies from the internet
    """
    raw_proxies = get_proxies.text.split("\n")
    proxies = {"http": f"http://{random.choice(raw_proxies)}"}
    print(proxies)
    return proxies


# This is a retry strategy with each try triggering a new proxy connection
# Helps to negate the effects of rate limiting and possibility of a dead proxy
retry_strategy = Retry(
    total=10,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=frozenset(["GET", "POST"]),
)
# Create an HTTP adapter with the retry strategy and mount it to session
adapter = HTTPAdapter(max_retries=retry_strategy)

# Create a new session object
session = requests.Session()
session.mount("https://", adapter)



def get_data():
    """
    Build a request to each platform and store the raw data in a dictionary
    """
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

        # This one is funny, we kind of automate request type process based on the request_data.json {request_type} value
        def request_by_type(method, **kwargs):
            request_method = getattr(session, method)
            response = request_method(**kwargs)
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
                    response = request_by_type(
                        platform["request_type"],
                        url=platform["url"],
                        headers=platform["headers"],
                        json=params_final,
                        proxies=setup_proxies(),
                        timeout=5,
                    )
                    print(
                        f"The type is: {type(response)}\n{type(response.text)}\n{response.status_code}"
                    )
                    if not response.text:
                        print(f"Empty response from {platform_name}")
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
                    # time.sleep(10)
                    response = request_by_type(
                        platform["request_type"],
                        url=platform["url"],
                        headers=headers_final,
                        params=params,
                        proxies=setup_proxies(),
                        timeout=5,
                    )
                    print(f"The type is: {type(response)}\n{response.text}")
                    raw_array[platform_name].append(
                        {
                            "location_name": location_name,
                            "raw_data": response.text,
                        }
                    )
    return raw_array


# Parsing the data, I wanted it to be universal, but guess each platform will have their own function
def wolt_parse():
    """
    Parsing Wolt data to a JSON
    """
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
    """
    Parsing Glovo data to a JSON
    """
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
    """
    Pushing the data to the PostgreSQL database
    """
    connect = psycopg2.connect(
        database=PG_DB_NAME,
        user=PG_USER,
        host=PG_DB_CONNECTION,
        password=PG_PASSWORD,
        port=PG_DB_PORT,
    )
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
    """
    Main function to run the script
    """
    get_data()
    #    glovo_parse()
    wolt_parse()
    with open(f"./export/export_{timestr}.json", "w", encoding="utf-8") as f:
        json.dump(export_array, f, ensure_ascii=False, indent=4)
    pg_export(export_array)


if __name__ == "__main__":
    main()
