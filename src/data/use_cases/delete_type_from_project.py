from src.domain.use_cases.i_delete_type_from_project import IDeleteTypeFromProject
from src.data.interface.i_project_type_repository import IProjectTypeRepository

class DeleteTypeFromProject(IDeleteTypeFromProject):

    def __init__(self, project_type_repository:IProjectTypeRepository) -> None:
        self.__project_type_repository = project_type_repository
    
    def delete(self, project_id:int) -> None:
        try:
            self.__project_type_repository.delete_all_from_project(
                project_id=project_id
            )
        except Exception as e:
            raise e from e