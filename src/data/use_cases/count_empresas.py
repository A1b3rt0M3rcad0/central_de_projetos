from src.domain.use_cases.i_count_empresas import ICountEmpresas
from src.data.interface.i_empresa_repository import IEmpresaRepository
from typing import Dict

class CountEmpresas(ICountEmpresas):

    def __init__(self, empresa_repository:IEmpresaRepository) -> None:
        self.__empresa_repository = empresa_repository
    
    def count(self) -> Dict[str, int]:
        try:
            return self.__empresa_repository.count_empresas()
        except Exception as e :
            raise e from e