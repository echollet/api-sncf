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


from db_sqlite3_itf import db_insert_lines, db_insert_lines_to_routes

from type_definitions import Line, Lines




def http_request(token:str, page:int)->str:

    url = 'https://api.navitia.io/v1/coverage/sncf/lines'

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


def get_all_lines(token:str)->Lines:
    ter_lines = []
    lines_to_routes = []

    nb_pages = get_pagination_lines()

    with tqdm(total=nb_pages) as bar:
        for page in range(1, nb_pages):
            single_page_lines = http_request(token, page)

            for line in single_page_lines["lines"]:
                
                # https://docs.python.org/3/howto/regex.html
                p = re.compile(':Train$')
                for physical_mode in line["physical_modes"]:
                    #print(physical_mode)
                    m = p.search(physical_mode["id"])

                    if m is not None:
                        route_ids = [ route["id"] for route in line["routes"] ]
                        ter_lines.append(Line(line["id"], line["name"], line["code"]))

                        for route_id in route_ids:
                            lines_to_routes.append((line["id"], route_id))
                   
            bar.update(1)

    return ter_lines, lines_to_routes


def get_pagination_lines()->int:
    url = 'https://api.navitia.io/v1/coverage/sncf/lines'
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
    lines, lines_to_routes = get_all_lines(API_TOKEN)

    #print(lines)
    #print(lines_to_routes)

    db_insert_lines(lines, DBNAME)
    db_insert_lines_to_routes(lines_to_routes, DBNAME)

