#
#
#

import logging
import requests

from typing import Dict, Any

def http_request_page(url:str, page:int, api_token_base64:str)->Dict[str,Any]:

    # e.g. : url = 'https://api.navitia.io/v1/coverage/sncf/stop_points'

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

    #headers = { 'Authorization' : 'Basic ZDNkYThlOGYtNmEzOS00ZTk4LTgzM2ItNzE5ZGRhYmQyM2EwOg==' }
    headers = { 'Authorization' : 'Basic '+ api_token_base64 }
    payload = { 'start_page' : page }
    
    x = requests.get(url, headers=headers, params=payload )
    logging.info(x.url)

    return x.json()

