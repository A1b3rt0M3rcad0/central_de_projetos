from src.domain.use_cases.i_delete_project_bairro import IDeleteProjectBairro
from src.data.interface.i_project_bairro_repository import IProjectBairroRepository

class DeleteProjectBairro(IDeleteProjectBairro):

    def __init__(self, project_bairro_repository:IProjectBairroRepository) -> None:
        self.__project_bairro_repository = project_bairro_repository
    
    def delete(self, project_id:int, bairro_id:int) -> None:
        try:
            self.__project_bairro_repository.delete(
                project_id=project_id,
                bairro_id=bairro_id
            )
        except Exception as e:
            raise e from e