class BaseAlreadyExistsError(Exception):

    def __init__(self, title:str, message:str, *args, **kwargs) -> None:
        self.title = title
        self.message = message
        super().__init__(*args, **kwargs)