from src.errors.use_cases.base.BaseError import BaseError

class TypesAlreadyExists(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='TypesAlreadyExists',
            message=message,
            *args,
            **kwargs
        )