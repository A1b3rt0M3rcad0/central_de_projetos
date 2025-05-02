from src.domain.use_cases.i_create_fiscal import ICreateFiscal
from src.data.interface.i_fiscal_repository import IFiscalRepository

class CreateFiscal(ICreateFiscal):

    def __init__(self, fiscal_repository:IFiscalRepository) -> None:
        self.__fiscal_repository = fiscal_repository
    
    def create(self, name:str) -> None:
        try:
            self.__fiscal_repository.insert(
                name=name
            )
        except Exception as e:
            raise e from e