from src.domain.use_cases.i_find_fiscal_by_name import IFindFiscalByName
from src.data.interface.i_fiscal_repository import IFiscalRepository
from src.domain.entities.fiscal import FiscalEntity

class FindFiscalByName(IFindFiscalByName):

    def __init__(self, fiscal_repository:IFiscalRepository) -> None:
        self.__fiscal_repository = fiscal_repository
    
    def find(self, name:str) -> FiscalEntity:
        try:
            fiscal = self.__fiscal_repository.find_by_name(
                name=name
            )
            return fiscal
        except Exception as e:
            raise e from e