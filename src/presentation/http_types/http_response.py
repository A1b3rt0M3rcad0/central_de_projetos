from typing import Dict

class HttpResponse:

    def __init__(self, status_code:int, body:Dict, headers:Dict|None=None) -> None:
        self.status_code = status_code
        self.body = body
        self.headers = headers
    
    def to_dict(self) -> Dict:
        return {
            'status_code': self.status_code,
            'headers': self.headers,
            'body': self.body,
        }