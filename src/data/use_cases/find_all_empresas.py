from src.domain.use_cases.i_find_all_empresas import IFindAllEmpresas
from src.domain.entities.empresa import EmpresaEntity
from src.data.interface.i_empresa_repository import IEmpresaRepository
from typing import List

class FindAllEmpresas(IFindAllEmpresas):

    def __init__(self, empresa_repository:IEmpresaRepository) -> None:
        self.__empresa_repository = empresa_repository
    
    def find(self) -> List[EmpresaEntity]:
        try:
            result = self.__empresa_repository.find_all()
            return result
        except Exception as e:
            raise e from e