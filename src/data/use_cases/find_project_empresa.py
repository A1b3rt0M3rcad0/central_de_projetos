from src.domain.use_cases.i_find_project_empresa import IFindProjectEmpresa
from src.data.interface.i_project_empresa_repository import IProjectEmpresaRepository
from src.domain.entities.project_empresa import ProjectEmpresaEntity

class FindProjectEmpresa(IFindProjectEmpresa):

    def __init__(self, project_empresa_repository:IProjectEmpresaRepository) -> None:
        self.__project_empresa_repository = project_empresa_repository
    
    def find(self, empresa_id:int, project_id:int) -> ProjectEmpresaEntity:
        try:
            result = self.__project_empresa_repository.find(
                empresa_id=empresa_id,
                project_id=project_id
            )
            return result
        except Exception as e:
            raise e from e