from src.errors.repository.error_on_update.__base_error_on_update import BaseErrorOnUpdate

class ErrorOnUpdateWorkProject(BaseErrorOnUpdate):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ErrorOnUpdateWorkProject',
            message=message,
            *args,
            **kwargs
        ) 