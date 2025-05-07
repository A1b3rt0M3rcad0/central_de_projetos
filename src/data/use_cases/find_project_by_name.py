from src.domain.entities.project import ProjectEntity
from src.domain.use_cases.i_find_project_by_name import IFindProjectByName
from src.data.interface.i_project_repository import IProjectRepository

class FindProjectByName(IFindProjectByName):

    def __init__(self, project_repository:IProjectRepository) -> None:
        self.__project_repository = project_repository
    
    def find(self, name:str) -> ProjectEntity:
        try:
            result = self.__project_repository.find_by_name(
                name=name
            )
            return result
        except Exception as e:
            raise e from e