from src.domain.use_cases.i_delete_fiscal import IDeleteFiscal
from src.data.interface.i_fiscal_repository import IFiscalRepository

class DeleteFiscal(IDeleteFiscal):

    def __init__(self, fiscal_repository:IFiscalRepository) -> None:
        self.__fiscal_repository = fiscal_repository
    
    def delete(self, name:str) -> None:
        try:
            self.__fiscal_repository.delete(
                name=name
            )
        except Exception as e:
            raise e from e