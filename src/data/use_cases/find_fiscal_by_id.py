from src.domain.entities.fiscal import FiscalEntity
from src.data.interface.i_fiscal_repository import IFiscalRepository
from src.domain.use_cases.i_find_fiscal_by_id import IFindFiscalById

class FindFiscalById(IFindFiscalById):

    def __init__(self, fiscal_repository:IFiscalRepository) -> None:
        self.__fiscal_repository = fiscal_repository
    
    def find(self, fiscal_id:int) -> FiscalEntity:
        try:
            result = self.__fiscal_repository.find_by_id(
                fiscal_id=fiscal_id
            )
            return result
        except Exception as e:
            raise e from e