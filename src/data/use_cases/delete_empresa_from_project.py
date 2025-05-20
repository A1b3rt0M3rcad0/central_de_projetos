from src.domain.use_cases.i_delete_empresa_from_project import IDeleteEmpresaFromProject
from src.data.interface.i_project_empresa_repository import IProjectEmpresaRepository

class DeleteEmpresaFromProject(IDeleteEmpresaFromProject):

    def __init__(self, project_empresa_repository:IProjectEmpresaRepository) -> None:
        self.__project_empresa_repository = project_empresa_repository
    
    def delete(self, project_id:int) -> None:
        try:
            self.__project_empresa_repository.delete_all_from_project(
                project_id=project_id
            )
        except Exception as e:
            raise e from e