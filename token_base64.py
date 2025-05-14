#
# Token to base64 interface
#

import base64


def token_to_base64(token:str):
    b = base64.b64encode(bytes(token, 'utf-8')) # bytes
    base64_str = b.decode('utf-8') # convert bytes to string

    return base64_str


