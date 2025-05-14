#
#
#

import logging
import re


from tqdm import tqdm


from type_definitions import StopPoint, StopPoints

from get_pagination import get_pagination
from get_http_pages import http_request_page

def get_data_stop_points(url:str, token_base64:str, maxpages:int)->StopPoints:
    stop_points = []
    nb_pages = min(get_pagination(url, token_base64), maxpages)

    with tqdm(total=nb_pages) as bar:
        for page in range(0, nb_pages):
            single_page_stop_points = http_request_page(url, page, token_base64)

            for stop_point in single_page_stop_points["stop_points"]:
                
                # https://docs.python.org/3/howto/regex.html
                p = re.compile(':Train$')
                m = p.search(stop_point["id"])

                if m is not None:
                    stop_points.append(StopPoint(stop_point["id"], stop_point["name"], stop_point["label"], 1))

                p = re.compile(':LongDistanceTrain$')
                m = p.search(stop_point["id"])

                if m is not None:
                    stop_points.append(StopPoint(stop_point["id"], stop_point["name"], stop_point["label"], 2))
                    
            bar.update(1)

    return stop_points


