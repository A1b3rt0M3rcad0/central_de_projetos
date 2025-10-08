from src.domain.use_cases.i_update_fiscal_phone import IUpdateFiscalPhone
from src.data.interface.i_fiscal_repository import IFiscalRepository

class UpdateFiscalPhone(IUpdateFiscalPhone):

    def __init__(self, fiscal_repository: IFiscalRepository) -> None:
        self.__fiscal_repository = fiscal_repository
    
    def update(self, name: str, phone: str) -> None:
        try:
            self.__fiscal_repository.update_phone(
                name=name,
                phone=phone
            )
        except Exception as e:
            raise e from e

