from src.domain.use_cases.i_delete_bairro_from_project import IDeleteBairroFromProject
from src.data.interface.i_project_bairro_repository import IProjectBairroRepository

class DeleteBairroFromProject(IDeleteBairroFromProject):

    def __init__(self, project_bairro_repository:IProjectBairroRepository) -> None:
        self.__project_bairro_repository = project_bairro_repository
    
    def delete(self, project_id:int) -> None:
        try:
            self.__project_bairro_repository.delete_all_from_project(
                project_id=project_id
            )
        except Exception as e:
            raise e from e