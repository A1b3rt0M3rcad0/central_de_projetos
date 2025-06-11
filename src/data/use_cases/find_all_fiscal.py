from src.domain.use_cases.i_find_all_fiscal import IFindAllFiscal
from typing import List
from src.domain.entities.fiscal import FiscalEntity
from src.data.interface.i_fiscal_repository import IFiscalRepository

class FindAllFiscal(IFindAllFiscal):

    def __init__(self, fiscal_repository:IFiscalRepository) -> None:
        self.__fiscal_repository = fiscal_repository
    
    def find(self) -> List[FiscalEntity]:
        try:
            result = self.__fiscal_repository.find_all()
            return result
        except Exception as e:
            raise e from e