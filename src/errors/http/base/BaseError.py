class BaseError(Exception):

    def __init__(self, status_code:int, title:str, message:str, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.status_code=status_code
        self.title=title
        self.message=message