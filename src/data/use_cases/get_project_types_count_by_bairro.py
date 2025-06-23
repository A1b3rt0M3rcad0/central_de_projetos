from src.domain.use_cases.i_get_project_types_count_by_bairro import IGetProjectTypesCountByBairro
from src.data.interface.i_project_type_repository import IProjectTypeRepository
from src.domain.entities.project_types_count_by_bairro import ProjectTypesCountByBairro

class GetProjectTypesCountByBairro(IGetProjectTypesCountByBairro):

    def __init__(self, project_type_repository:IProjectTypeRepository) -> None:
        self.__project_type_repository = project_type_repository
    
    def get(self) -> ProjectTypesCountByBairro:
        try:
            result = self.__project_type_repository.get_project_types_count_by_bairro()
            return result
        except Exception as e:
            raise e from e