from src.errors.repository.error_on_update.__base_error_on_update import BaseErrorOnUpdate

class ErrorOnUpdateEmpresaFromProject(BaseErrorOnUpdate):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ErrorOnUpdateEmpresaFromProject',
            message=message,
            *args,
            **kwargs
        )