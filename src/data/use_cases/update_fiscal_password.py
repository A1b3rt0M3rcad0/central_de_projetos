from src.domain.use_cases.i_update_fiscal_password import IUpdateFiscalPassword
from src.data.interface.i_fiscal_repository import IFiscalRepository
from src.security.value_objects.hashed_password import HashedPassword

class UpdateFiscalPassword(IUpdateFiscalPassword):

    def __init__(self, fiscal_repository: IFiscalRepository) -> None:
        self.__fiscal_repository = fiscal_repository
    
    def update(self, name: str, password: HashedPassword) -> None:
        try:
            self.__fiscal_repository.update_password(
                name=name,
                password=password
            )
        except Exception as e:
            raise e from e

