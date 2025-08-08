from src.errors.use_cases.__base.base_use_case_error import BaseUseCaseError

class DeleteWorkProjectError(BaseUseCaseError):
    def __init__(self, message: str) -> None:
        super().__init__(title="Delete Work Project Error", message=message) 