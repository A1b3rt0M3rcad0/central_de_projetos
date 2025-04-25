from src.errors.use_cases.base.BaseError import BaseError

class CreateProjectError(BaseError):

    def __init__(self, message:str, *args, **kwargs):
        super().__init__(
            title='CreateProjectError',
            message=message,
            *args, 
            **kwargs
        )