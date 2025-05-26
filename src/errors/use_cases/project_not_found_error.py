from src.errors.use_cases.__base.base_use_case_error import BaseUseCaseError

class ProjectNotFoundError(BaseUseCaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ProjectNotFoundError',
            message=message,
            *args,
            **kwargs
        )