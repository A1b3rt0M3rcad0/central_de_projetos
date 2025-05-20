from src.domain.use_cases.i_create_project_empresa import ICreateProjectEmpresa
from src.data.interface.i_project_empresa_repository import IProjectEmpresaRepository

class CreateProjectEmpresa(ICreateProjectEmpresa):

    def __init__(self, project_empresa_repository:IProjectEmpresaRepository) -> None:
        self.__project_empresa_repository = project_empresa_repository
    
    def create(self, empresa_id:int, project_id:int) -> None:
        try:
            self.__project_empresa_repository.insert(
                empresa_id=empresa_id,
                project_id=project_id
            )
        except Exception as e:
            raise e from e