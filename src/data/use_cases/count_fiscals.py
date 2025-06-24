from src.domain.use_cases.i_count_fiscals import ICountFiscals
from src.data.interface.i_fiscal_repository import IFiscalRepository
from typing import Dict

class CountFiscals(ICountFiscals):

    def __init__(self, fiscal_repository:IFiscalRepository) -> None:
        self.__fiscal_repository= fiscal_repository
    
    def count(self) -> Dict[str, int]:
        try:
            return self.__fiscal_repository.count_fiscals()
        except Exception as e:
            raise e from e