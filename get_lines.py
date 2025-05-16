#
#
#

import re

from tqdm import tqdm
from typing import Dict, Any, Tuple, List


from type_definitions import Line, Lines, LineId, RouteId

from get_pagination import get_pagination
from get_http_pages import http_request_page


def get_data_lines(url:str, token_base64:str, maxpages:int)->Tuple[Lines, List[Tuple[LineId, RouteId]]]:
    ter_lines = []
    lines_to_routes = []

    nb_pages = min(get_pagination(url, token_base64), maxpages) if maxpages > 0 else get_pagination(url, token_base64)

    with tqdm(total=nb_pages) as bar:
        for page in range(0, nb_pages):
            single_page_lines : Dict[str,Any] = http_request_page(url, page, token_base64)

            for line in single_page_lines["lines"]:
                
                # https://docs.python.org/3/howto/regex.html
                p = re.compile(':Train$')
                for physical_mode in line["physical_modes"]:
                    #print(physical_mode)
                    m = p.search(physical_mode["id"])

                    if m is not None:
                        route_ids = [ route["id"] for route in line["routes"] ]
                        ter_lines.append(Line(line["id"], line["name"], line["code"], line["network"]["id"]))

                        for route_id in route_ids:
                            lines_to_routes.append((line["id"], route_id))
                   
            bar.update(1)

    return ter_lines, lines_to_routes


