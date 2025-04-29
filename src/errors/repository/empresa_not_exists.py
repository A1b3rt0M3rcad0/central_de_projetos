from src.errors.use_cases.base.BaseError import BaseError

class EmpresaNotExists(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='EmpresaNotExists',
            message=message,
            *args,
            **kwargs
        )