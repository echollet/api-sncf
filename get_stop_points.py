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
from collections import namedtuple


import sqlite3_itf as sql


StopPoint = namedtuple("StopPoint", "id name label")
StopPoints = namedtuple("StopPoints", "train_stops long_dist_train_stops")


API_TOKEN="d3da8e8f-6a39-4e98-833b-719ddabd23a0"

def http_request(token:str, page:int)->str:

    url = 'https://api.navitia.io/v1/coverage/sncf/stop_points'

    # https://numerique.sncf.com/startup/api/
    # https://doc.navitia.io/#authentication
    # https://docs.python-requests.org/en/latest/user/quickstart/#custom-headers
    # https://docs.python-requests.org/en/latest/user/quickstart/#passing-parameters-in-urls

    headers = { 'Authorization' : 'Basic ZDNkYThlOGYtNmEzOS00ZTk4LTgzM2ItNzE5ZGRhYmQyM2EwOg==' }
    payload = { 'start_page' : page }
    
    x = requests.get(url, headers=headers, params=payload )
    logging.info(x.url)

    return x.json()


def get_all_stops(token:str)->StopPoints:
    train_stop_points = []
    longdist_train_stop_points = []

    #for i in range(1, 255):
    for page in range(1, 4):
        single_page_stop_points = http_request(token, page)

        for stop_point in single_page_stop_points["stop_points"]:
            
            # https://docs.python.org/3/howto/regex.html
            p = re.compile(':Train$')
            m = p.search(stop_point["id"])

            if m is not None:
                train_stop_points.append(StopPoint(stop_point["id"], stop_point["name"], stop_point["label"]))

        for stop_point in single_page_stop_points["stop_points"]:
            
            p = re.compile(':LongDistanceTrain$')
            m = p.search(stop_point["id"])

            if m is not None:
                longdist_train_stop_points.append((stop_point["id"], stop_point["name"], stop_point["label"]))

    #print(train_stop_points)
    #print(longdist_train_stop_points)

    return StopPoints(train_stop_points, longdist_train_stop_points)


def insert_stop_points_in_db(stop_points, conn):
    for stop_point in stop_points.train_stops:
        sql.insert_train_stop(conn, (stop_point.id, stop_point.name, stop_point.label, 1))
    return


if __name__ == "__main__":

    LOGLEVEL='INFO'
    #LOGLEVEL='DEBUG'

    logger = logging.getLogger(__name__)
    numeric_level = getattr(logging, LOGLEVEL.upper(), None)
    #logging.basicConfig(filename='./process.log', encoding='utf-8', level=numeric_level)
    logging.basicConfig(filename='./process.log', level=numeric_level)

    #logging.info("Syst path : {}".format(sys.path))

    load_dotenv()
    API_TOKEN = os.environ.get('API_TOKEN')
    DBNAME = os.environ.get('DBNAME')

    logging.info(API_TOKEN)
    logging.info(DBNAME)

    stop_points = get_all_stops(API_TOKEN)

    print(stop_points)

    conn = sql.create_connection(DBNAME)

    insert_stop_points_in_db(stop_points, conn)

