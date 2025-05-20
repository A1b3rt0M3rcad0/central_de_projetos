from src.domain.use_cases.i_delete_project_type import IDeleteProjectType
from src.data.interface.i_project_type_repository import IProjectTypeRepository

class DeleteProjectType(IDeleteProjectType):

    def __init__(self, project_type_repository:IProjectTypeRepository) -> None:
        self.__project_type_repository = project_type_repository
    
    def delete(self, project_id:int, type_id:int) -> None:
        try:
            self.__project_type_repository.delete(
                project_id=project_id,
                type_id=type_id
            )
        except Exception as e:
            raise e from e