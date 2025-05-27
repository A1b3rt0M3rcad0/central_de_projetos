from src.errors.repository.error_on_update.__base_error_on_update import BaseErrorOnUpdate

class ErrorOnUpdateBairroFromProject(BaseErrorOnUpdate):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ErrorOnUpdateBairroFromProject',
            message=message,
            *args,
            **kwargs
        )