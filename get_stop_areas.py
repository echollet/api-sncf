#
#
#


from tqdm import tqdm
from typing import Dict, Any

from type_definitions import StopArea, StopAreas

from get_pagination import get_pagination
from get_http_pages import http_request_page


def get_data_stop_areas(url:str, token_base64:str, maxpages:int)->StopAreas:

    stop_areas = []
    nb_pages = min(get_pagination(url, token_base64), maxpages) if maxpages > 0 else get_pagination(url, token_base64)

    with tqdm(total=nb_pages) as bar:
        for page in range(0, nb_pages):
            single_page_stop_areas : Dict[str,Any]  = http_request_page(url, page, token_base64)

            for stop_area in single_page_stop_areas["stop_areas"]:
                stop_areas.append(StopArea(stop_area["id"], stop_area["name"], stop_area["label"]))

            bar.update(1)

    return stop_areas


