from src.errors.use_cases.__base.base_use_case_error import BaseUseCaseError

class CreateProjectError(BaseUseCaseError):

    def __init__(self, message:str, *args, **kwargs):
        super().__init__(
            title='CreateProjectError',
            message=message,
            *args, 
            **kwargs
        )