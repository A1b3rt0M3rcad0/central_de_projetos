from src.errors.repository.error_on_insert.__base_error_on_insert import BaseErrorOnInsert

class ErrorOnInsertWorkProject(BaseErrorOnInsert):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ErrorOnInsertWorkProject',
            message=message,
            *args,
            **kwargs
        ) 