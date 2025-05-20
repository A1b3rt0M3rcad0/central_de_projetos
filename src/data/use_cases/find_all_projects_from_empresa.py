from src.domain.use_cases.i_find_all_projects_from_empresa import IFindAllProjectsfromEmpresa
from src.data.interface.i_project_empresa_repository import IProjectEmpresaRepository
from src.domain.entities.project_empresa import ProjectEmpresaEntity
from typing import List

class FindAllProjectsFromEmpresa(IFindAllProjectsfromEmpresa):

    def __init__(self, project_empresa_repository:IProjectEmpresaRepository) -> None:
        self.__project_empresa_repository = project_empresa_repository
    
    def find(self, empresa_id:int) -> List[ProjectEmpresaEntity]:
        try:
            result = self.__project_empresa_repository.find_all_from_empresa(
                empresa_id=empresa_id
            )
            return result
        except Exception as e:
            raise e from e