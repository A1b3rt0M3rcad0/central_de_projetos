from src.errors.use_cases.__base.base_use_case_error import BaseUseCaseError

class FiscalInactiveError(BaseUseCaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='FiscalInactiveError',
            message=message,
            *args,
            **kwargs
        )

