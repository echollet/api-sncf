#
#
#

import re

from tqdm import tqdm

from typing import Dict, Any, Tuple, List
from type_definitions import StopPointId, LineId

from get_pagination import get_pagination
from get_http_pages import http_request_page

from db_sqlite3_itf import db_select_stop_points


def get_data_stop_point_to_line(url:str, token_base64:str, maxstops:int, dbname:str)->List[List[Tuple[StopPointId,LineId]]]:

    stop_points_lines = []

    stop_point_ids = db_select_stop_points(dbname)

    nb_stops = min(maxstops, len(stop_point_ids)) if maxstops > 0 else len(stop_point_ids)

    stop_point_ids = stop_point_ids[0:nb_stops]

    with tqdm(total=len(stop_point_ids)) as bar: 

        for stop_point_id in stop_point_ids :

            url_stop_point = url + "/{}".format(stop_point_id) + "/lines"

            nb_pages = get_pagination(url_stop_point, token_base64)

            stop_point_line_ids = []

            for page in range(0, nb_pages):
                lines : Dict[str,Any]  = http_request_page(url_stop_point, page, token_base64)      

                for line in lines["lines"]:
                    stop_point_line_ids.append((stop_point_id, line["id"]))

            stop_points_lines.append(stop_point_line_ids)    
        
            bar.update(1)


    return stop_points_lines





