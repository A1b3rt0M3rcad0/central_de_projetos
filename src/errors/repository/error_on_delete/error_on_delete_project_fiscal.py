from src.errors.repository.error_on_delete.__base_error_on_delete import BaseErrorOnDelete

class ErrorOnDeleteProjectFiscal(BaseErrorOnDelete):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ErrorOnDeleteProjectFiscal',
            message=message,
            *args,
            **kwargs
        )