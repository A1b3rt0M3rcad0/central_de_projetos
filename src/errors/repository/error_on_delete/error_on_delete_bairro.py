from src.errors.repository.error_on_delete.__base_error_on_delete import BaseErrorOnDelete

class ErrorOnDeleteBairro(BaseErrorOnDelete):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title=self.__class__.__name__,
            message=message,
            *args,
            **kwargs
        )