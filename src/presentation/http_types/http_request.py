from typing import Dict

class HttpRequest:

    def __init__(self,
                 headers:Dict|None = None,
                 body:Dict|None = None,
                 query_params:Dict|None = None,
                 path_params:Dict|None = None,
                 url:str|None = None,
                 ipv4:str|None = None
                 ) -> None:
        self.headers = headers
        self.body = body
        self.query_params = query_params
        self.path_params = path_params
        self.url = url
        self.ipv4 = ipv4