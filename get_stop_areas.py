#
#
#

import os
import sys
import logging
import requests
import json
import re

from dotenv import load_dotenv

from tqdm import tqdm

from db_sqlite3_itf import db_insert_stop_areas

from type_definitions import StopArea, StopAreas




def http_request(token:str, page:int)->str:

    url = 'https://api.navitia.io/v1/coverage/sncf/stop_areas'

    # https://numerique.sncf.com/startup/api/
    # https://docs.python-requests.org/en/latest/user/quickstart/#custom-headers
    # https://docs.python-requests.org/en/latest/user/quickstart/#passing-parameters-in-urls

    #
    # https://doc.navitia.io/#authentication
    # https://datatracker.ietf.org/doc/html/rfc2617#section-2

    #
    # to get api token's Base64 encoding
    # see : https://www.base64encode.org/
    #
    # input : <token>+':'  
    # e.g : 
    # d3da8e8f-6a39-4e98-833b-719ddabd23a0:
    # => ZDNkYThlOGYtNmEzOS00ZTk4LTgzM2ItNzE5ZGRhYmQyM2EwOg==
    #

    headers = { 'Authorization' : 'Basic ZDNkYThlOGYtNmEzOS00ZTk4LTgzM2ItNzE5ZGRhYmQyM2EwOg==' }
    payload = { 'start_page' : page }
    
    x = requests.get(url, headers=headers, params=payload )
    logging.info(x.url)

    return x.json()


def get_all_stop_areas(token:str)->StopAreas:

    stop_areas = []

    nb_pages = get_pagination_stop_areas()
    with tqdm(total=nb_pages) as bar:
        for page in range(0, nb_pages):
            single_page_stop_areas = http_request(token, page)

            for stop_area in single_page_stop_areas["stop_areas"]:
                stop_areas.append(StopArea(stop_area["id"], stop_area["name"], stop_area["label"]))
            bar.update(1)

    return stop_areas


def get_pagination_stop_areas()->int:
    url = 'https://api.navitia.io/v1/coverage/sncf/stop_areas'
    headers = { 'Authorization' : 'Basic ZDNkYThlOGYtNmEzOS00ZTk4LTgzM2ItNzE5ZGRhYmQyM2EwOg==' }
    payload = {}
    
    x = requests.get(url, headers=headers, params=payload )
    logging.info(x.url)

    json_data = x.json()
    total_result = json_data["pagination"]["total_result"]
    items_per_page = json_data["pagination"]["items_per_page"]

    nb_pages = int(total_result / items_per_page)
    if total_result % items_per_page > 0:
        nb_pages+=1
    logging.info("nb_pages : {}".format(nb_pages))

    return nb_pages



if __name__ == "__main__":

    #
    # init logger
    #
    LOGLEVEL='INFO'
    #LOGLEVEL='DEBUG'

    logger = logging.getLogger(__name__)
    numeric_level = getattr(logging, LOGLEVEL.upper(), None)
    logging.basicConfig(filename='./process.log', level=numeric_level)

    #
    # load .env
    #
    load_dotenv()
    API_TOKEN = os.environ.get('API_TOKEN')
    DBNAME = os.environ.get('DBNAME')

    logging.info(API_TOKEN)
    logging.info(DBNAME)

    #
    # get stop_points
    #
    stop_areas = get_all_stop_areas(API_TOKEN)

    #print(stop_areas)

    db_insert_stop_areas(stop_areas, DBNAME)

