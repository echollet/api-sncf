#
#
#

import os
import logging
import argh

from dotenv import load_dotenv

from db_sqlite3_itf import db_insert_stop_points
from token_base64 import token_to_base64
from get_stop_points import get_data_stop_points


#
# argh commands
#

def get_stop_points(arg1: str, *args, maxpages: int, exec: bool = False) :

    logging.info("arguments : {}".format([arg1, args, maxpages, exec]))

    url = 'https://api.navitia.io/v1/coverage/sncf/stop_points'

    stop_points = get_data_stop_points(url, API_TOKEN_BASE64, maxpages)
    #print(stop_points)
    if exec :
        db_insert_stop_points(stop_points, DBNAME)


def get_stop_areas(arg1: str, *args, maxpages: int, exec: bool = False) :
    logging.info("arguments : {}".format([arg1, args, maxpages, exec]))

    return
    

def get_lines(arg1: str, *args, maxpages: int, exec: bool = False) :
    logging.info("arguments : {}".format([arg1, args, maxpages, exec]))

    return
    

def get_routes(arg1: str, *args, maxpages: int, exec: bool = False) :
    logging.info("arguments : {}".format([arg1, args, maxpages, exec]))

    return
    


#
# main
#

API_TOKEN_BASE64 = ""
parser=argh.ArghParser()
parser.add_commands([get_stop_points, get_stop_areas, get_lines, get_routes])


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
    API_TOKEN_BASE64 = token_to_base64(API_TOKEN+':')

    DBNAME = os.environ.get('DBNAME')

    logging.info("API_TOKEN {}".format(API_TOKEN))
    logging.info("API_TOKEN_BASE64 {}".format(API_TOKEN_BASE64))
    logging.info("DBNAME {}".format(DBNAME))

    parser.dispatch()



