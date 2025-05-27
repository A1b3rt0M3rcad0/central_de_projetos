from src.errors.repository.error_on_update.__base_error_on_update import BaseErrorOnUpdate

class ErroronUpdateFiscal(BaseErrorOnUpdate):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title=self.__class__.__name__,
            message=message,
            *args,
            **kwargs
        )