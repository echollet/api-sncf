#
#
#

import os
import logging
import argh

from typing import cast

from dotenv import load_dotenv

from db_sqlite3_itf import \
    db_insert_stop_points, db_insert_stop_areas, db_insert_lines, db_insert_lines_to_routes, \
    db_insert_routes, db_insert_networks

from token_base64 import token_to_base64
from get_stop_points import get_data_stop_points
from get_stop_areas import get_data_stop_areas
from get_lines import get_data_lines
from get_routes import get_data_routes
from get_networks import get_data_networks


#
# argh commands
#

def get_stop_points(arg1: str, *args, maxpages: int, exec: bool = False) :

    logging.info("arguments : {}".format([arg1, args, maxpages, exec]))

    url = 'https://api.navitia.io/v1/coverage/sncf/stop_points'

    stop_points = get_data_stop_points(url, API_TOKEN_BASE64, maxpages)

    if exec :
        db_insert_stop_points(stop_points, DBNAME)


def get_stop_areas(arg1: str, *args, maxpages: int, exec: bool = False) :

    logging.info("arguments : {}".format([arg1, args, maxpages, exec]))

    url = 'https://api.navitia.io/v1/coverage/sncf/stop_areas'

    stop_areas = get_data_stop_areas(url, API_TOKEN_BASE64, maxpages)

    if exec :
        db_insert_stop_areas(stop_areas, DBNAME)
    return
    

def get_lines(arg1: str, *args, maxpages: int, exec: bool = False) :
    logging.info("arguments : {}".format([arg1, args, maxpages, exec]))

    url = 'https://api.navitia.io/v1/coverage/sncf/lines'

    lines, line_to_routes = get_data_lines(url, API_TOKEN_BASE64, maxpages)

    if exec :
        db_insert_lines(lines, DBNAME)
        db_insert_lines_to_routes(line_to_routes, DBNAME)
    return
    

def get_routes(arg1: str, *args, maxpages: int, exec: bool = False) :
    logging.info("arguments : {}".format([arg1, args, maxpages, exec]))

    url = 'https://api.navitia.io/v1/coverage/sncf/routes'

    routes = get_data_routes(url, API_TOKEN_BASE64, maxpages)
    
    if exec :
        db_insert_routes(routes, DBNAME)

    return
    

def get_networks(arg1: str, *args, maxpages: int, exec: bool = False) :
    logging.info("arguments : {}".format([arg1, args, maxpages, exec]))

    url = 'https://api.navitia.io/v1/coverage/sncf/networks'

    routes = get_data_networks(url, API_TOKEN_BASE64, maxpages)
    
    if exec :
        db_insert_networks(routes, DBNAME)

    return


#
# main
#

API_TOKEN_BASE64 = ""
parser=argh.ArghParser()
parser.add_commands([get_networks, get_stop_points, get_stop_areas, get_lines, get_routes])


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
    API_TOKEN : str = cast(str,os.environ.get('API_TOKEN')) # Optional[str] -> str
    API_TOKEN_BASE64 = token_to_base64(API_TOKEN+':')

    DBNAME : str = cast(str, os.environ.get('DBNAME')) # Optional[str] -> str

    logging.info("API_TOKEN {}".format(API_TOKEN))
    logging.info("API_TOKEN_BASE64 {}".format(API_TOKEN_BASE64))
    logging.info("DBNAME {}".format(DBNAME))

    parser.dispatch()



