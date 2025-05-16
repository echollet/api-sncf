#
#
#

import logging
import requests

from typing import Dict


def get_pagination(url:str, token_base64:str)->int:
    
    headers = { 'Authorization' : 'Basic '+ token_base64 }
    #headers = { 'Authorization' : 'Basic ZDNkYThlOGYtNmEzOS00ZTk4LTgzM2ItNzE5ZGRhYmQyM2EwOg==' }
    payload : Dict[ str,str] = {}

    x = requests.get(url, headers=headers, params=payload)
    #logging.info("get_pagination: url {}".format(x.url))

    json_data = x.json()
    #logging.info("get_pagination: json_data {}".format(json_data))

    total_result = json_data["pagination"]["total_result"]
    items_per_page = json_data["pagination"]["items_per_page"]

    nb_pages = int(total_result / items_per_page)
    if total_result % items_per_page > 0:
        nb_pages+=1

    logging.info("url {} => nb_pages : {}".format(url, nb_pages))

    return nb_pages


