from src.errors.use_cases.__base.base_use_case_error import BaseUseCaseError

class FiscalDocumentNotFoundError(BaseUseCaseError):
    def __init__(self, message: str) -> None:
        super().__init__(title="Fiscal Document Not Found", message=message) 