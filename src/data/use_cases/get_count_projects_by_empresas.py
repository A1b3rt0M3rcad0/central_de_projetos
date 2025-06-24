from src.data.interface.i_empresa_repository import IEmpresaRepository
from src.domain.use_cases.i_get_count_projects_by_empresas import IGetCountProjectsByEmpresas
from typing import Dict

class GetCountProjectsByEmpresas(IGetCountProjectsByEmpresas):

    def __init__(self, empresa_repository:IEmpresaRepository) -> None:
        self.__empresa_repository= empresa_repository
    
    def get(self) -> Dict[str, int]:
        try:
            return self.__empresa_repository.get_count_projects_by_empresas()
        except Exception as e:
            raise e from e