from src.domain.use_cases.i_delete_project_empresa import IDeleteProjectEmpresa
from src.data.interface.i_project_empresa_repository import IProjectEmpresaRepository

class DeleteProjectEmpresa(IDeleteProjectEmpresa):

    def __init__(self, project_empresa_repository:IProjectEmpresaRepository) -> None:
        self.__project_empresa_repository = project_empresa_repository
    
    def delete(self, empresa_id:int, project_id:int) -> None:
        try:
            self.__project_empresa_repository.delete(
                empresa_id=empresa_id,
                project_id=project_id
            )
        except Exception as e:
            raise e from e