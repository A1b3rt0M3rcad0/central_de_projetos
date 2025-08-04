from src.errors.repository.error_on_find.__base_error_on_find import BaseErrorOnFind

class ErrorOnFindWorkProject(BaseErrorOnFind):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ErrorOnFindWorkProject',
            message=message,
            *args,
            **kwargs
        ) 