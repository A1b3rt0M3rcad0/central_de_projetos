class HttpBaseError(Exception):

    def __init__(self, status_code:int, title:str, message:str) -> None:
        self.status_code = status_code
        self.title = title
        self.message = message