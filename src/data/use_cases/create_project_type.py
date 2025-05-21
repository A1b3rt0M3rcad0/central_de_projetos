from src.domain.use_cases.i_create_project_type import ICreateProjectType
from src.data.interface.i_project_type_repository import IProjectTypeRepository

class CreateProjectType(ICreateProjectType):

    def __init__(self, project_type_repository:IProjectTypeRepository) -> None:
        self.__project_type_repository = project_type_repository
    
    def create(self, project_id:int, type_id:int) -> None:
        try:
            self.__project_type_repository.insert(
                project_id=project_id,
                type_id=type_id
            )
        except Exception as e:
            raise e from e