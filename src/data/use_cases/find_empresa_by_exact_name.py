from src.domain.use_cases.i_find_empresa_by_exact_name import IFindEmpresaByExactName
from src.data.interface.i_empresa_repository import IEmpresaRepository
from src.domain.entities.empresa import EmpresaEntity

class FindEmpresaByExactName(IFindEmpresaByExactName):

    def __init__(self, empresa_repository:IEmpresaRepository) -> None:
        self.__empresa_repository = empresa_repository
    
    def find(self, name:str) -> EmpresaEntity:
        try:
            result = self.__empresa_repository.find_by_name(
                name=name
            )
            return result
        except Exception as e:
            raise e from e