from src.errors.use_cases.base.BaseError import BaseError

class InvalidAssociationError(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='InvalidAssociationError',
            message=message,
            *args,
            **kwargs
        )