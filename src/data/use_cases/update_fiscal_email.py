from src.domain.use_cases.i_update_fiscal_email import IUpdateFiscalEmail
from src.data.interface.i_fiscal_repository import IFiscalRepository
from src.domain.value_objects.email import Email

class UpdateFiscalEmail(IUpdateFiscalEmail):

    def __init__(self, fiscal_repository: IFiscalRepository) -> None:
        self.__fiscal_repository = fiscal_repository
    
    def update(self, name: str, email: Email) -> None:
        try:
            self.__fiscal_repository.update_email(
                name=name,
                email=email
            )
        except Exception as e:
            raise e from e

