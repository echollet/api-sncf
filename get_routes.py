#
#
#


from tqdm import tqdm
from type_definitions import Route, Routes

from get_pagination import get_pagination
from get_http_pages import http_request_page


def get_data_routes(url:str, token_base64:str, maxpages:int)->Routes:
    routes = []

    nb_pages = min(get_pagination(url, token_base64), maxpages) if maxpages > 0 else get_pagination(url, token_base64)

    with tqdm(total=nb_pages) as bar:
        for page in range(0, nb_pages):
            single_page_routes = http_request_page(url, page, token_base64)

            for route in single_page_routes["routes"]:
                routes.append(Route(route["id"], route["name"], route["line"]["id"]))
                   
            bar.update(1)

    return routes


