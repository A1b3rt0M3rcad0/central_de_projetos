from src.data.interface.i_fiscal_repository import IFiscalRepository
from src.domain.use_cases.i_update_fiscal_name import IUpdateFiscalName

class UpdateFiscalName(IUpdateFiscalName):

    def __init__(self, fiscal_repository:IFiscalRepository) -> None:
        self.__fiscal_repository = fiscal_repository
    
    def update(self, name:str, new_name:str) -> None:
        try:
            self.__fiscal_repository.update(
                name=name,
                new_name=new_name
            )
        except Exception as e:
            raise e from e