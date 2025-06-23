from src.domain.use_cases.i_get_project_counts_by_bairro import IGetProjectCountsByBairro
from src.data.interface.i_project_bairro_repository import IProjectBairroRepository
from src.domain.entities.project_bairro_summary import ProjectBairroSummary

class GetProjectCountsByBairro(IGetProjectCountsByBairro):

    def __init__(self, project_bairro_repository:IProjectBairroRepository) -> None:
        self.__project_bairro_repository = project_bairro_repository
    
    def get(self) -> ProjectBairroSummary:
        try:
            result = self.__project_bairro_repository.get_project_counts_by_bairro()
            return result
        except Exception as e:
            raise e from e