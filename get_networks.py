#
#
#


from tqdm import tqdm

from typing import Dict, Any

from type_definitions import Network, Networks

from get_pagination import get_pagination
from get_http_pages import http_request_page


def get_data_networks(url:str, token_base64:str, maxpages:int)->Networks:

    networks = []
    nb_pages = min(get_pagination(url, token_base64), maxpages) if maxpages > 0 else get_pagination(url, token_base64)

    with tqdm(total=nb_pages) as bar:
        for page in range(0, nb_pages):
            single_page_networks : Dict[str,Any] = http_request_page(url, page, token_base64)

            for network in single_page_networks["networks"]:
                networks.append(Network(network["id"], network["name"]))

            bar.update(1)

    return networks